#!/usr/bin/env python
# coding=utf-8

# lachesis automates the segmentation of a transcript into closed captions
#
# Copyright (C) 2016-2017, Alberto Pettarin (www.albertopettarin.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import cPickle as pickle
import io
import os
import pycrfsuite
import sys

from lachesis.downloaders import Downloader
from lachesis.elements import Span
from lachesis.language import Language
from lachesis.nlpwrappers import NLPEngine
import lachesis.globalfunctions as gf

ANSI_ERROR = u"\033[91m"
ANSI_OK = u"\033[92m"
ANSI_WARNING = u"\033[93m"
ANSI_END = u"\033[0m"


def tokens_to_features(tokens, forward=5, max_chars_per_line=42, debug=False):
    """
    Convert a sequence of tokens into a sequence of features,
    that is, a list of dicts, each dict containing
    the features associated to the corresponding token
    in the input sequence.
    """
    feature_sequence = []

    # for debugging purposes, use this simple function
    if debug:
        for idx, token in enumerate(tokens):
            feature_sequence.append({
                "idx": idx,
                "word": token.raw,
                "ws": token.trailing_whitespace,
                "pos": token.upos_tag,
            })
        return feature_sequence

    # raw string of the word
    words = [t.raw for t in tokens]
    # POS of the word
    poses = [t.upos_tag for t in tokens]
    # bool, True if word has trailing whitespace
    wses = [t.trailing_whitespace for t in tokens]

    n = len(tokens)
    # length of the word, including trailing space, if present
    lens = [len(w) + (1 if ws else 0) for w, ws in zip(words, wses)]
    # cumulative length, before the i-th word
    clens = [0 for i in range(n)]
    # cumulative length, including i-th word
    alens = [lens[0] for i in range(n)]
    for i in range(1, n):
        clens[i] = lens[i] + clens[i - 1]
        alens[i] += clens[i]

    # pad forward to simplify later index access
    bf_poses = poses + [u"EOSP"] * forward
    bf_lens = lens + [1000] * forward
    bf_clens = clens + [1000] * forward
    bf_alens = alens + [1000] * forward

    for idx in range(n):
        token_features = {
            "bias": 0,
            "idx": idx,
            "bos": (idx == 0),
            "word": words[idx],
            "pos": poses[idx],
            "ws": wses[idx],
            "len": lens[idx],
            "clen": clens[idx] > max_chars_per_line,
            "alen": alens[idx] > max_chars_per_line,
        }
        for f in range(1, forward + 1):
            # create new pos-0+1, pos-0+2, ..., pos-0+5 keys
            # by concatenating the POS of the POS values
            # of the subsequent tokens
            token_features["pos-0+%d" % f] = u"-".join(bf_poses[idx:(idx + f)])
        for sidx in range(idx + 1, idx + 1 + forward):
            # also adds the POS, clen, alen of the next forward tokens
            token_features["pos+%d" % f] = bf_poses[sidx]
            # NOTE: disabled, as it is not useful
            # token_features["len+%d" % f] = bf_lens[sidx]
            token_features["clen+%d" % f] = (bf_clens[sidx] > max_chars_per_line)
            token_features["alen+%d" % f] = (bf_alens[sidx] > max_chars_per_line)
        # print(token_features)
        feature_sequence.append(token_features)
    return feature_sequence


class CRFTrainer(object):
    """
    TBW
    """

    PARAMETERS = {
        "max_iterations": 50,
        "feature.possible_transitions": True,
    }
    """ Parameters for the trainer from pycrfsuite """

    VERBOSE = False
    """ Verbosity of the trainer """

    LABEL_NOT_LAST = u"_"
    """ Label for a token that is not the last of a line """

    LABEL_LAST = u"E"
    """ Label for a token that is the last of a line """

    def __init__(
        self,
        language,
        nlpwrapper=u"pattern",
        downloader=u"youtube",
        parameters=PARAMETERS,
        verbose=VERBOSE
    ):
        self.language = language
        self.nlpwrapper = nlpwrapper
        self.downloader = downloader
        self.parameters = parameters
        self.verbose = verbose
        self.nlpe = NLPEngine(preload=[(self.language, self.nlpwrapper)])
        self.train_data = None
        self.trainer = None

    def _read_files(self, input_file_paths):
        def _annotated_sentence_to_lines(tokens):
            lines = []
            cl = []
            for t in tokens:
                if t.is_special:
                    if len(cl) > 0:
                        lines.append(cl)
                        cl = []
                else:
                    cl.append(t)
            if len(cl) > 0:
                lines.append(cl)
            return lines

        examples = []
        for ifp in input_file_paths:
            print(u".")
            if os.path.isfile(ifp):
                doc = Downloader.read_closed_captions(ifp, {u"downloader": u"youtube"})
                self.nlpe.analyze(doc, wrapper=self.nlpwrapper)
                for sentence in doc.sentences:
                    # print(sentence.string(eol=u"|", eos=u"").strip())
                    # sentence is a Span object
                    # sentence.elements is a list of Token objects
                    lines = _annotated_sentence_to_lines(sentence.elements)
                    for line in lines:
                        # all tokens get "add" label,
                        # except the last one, which gets the "end" label
                        labels = [self.LABEL_NOT_LAST] * len(line)
                        labels[-1] = self.LABEL_LAST
                        # convert the list of
                        features = tokens_to_features(line)
                        example = (features, labels)
                        # print(example)
                        examples.append(example)
        return examples

    def load_data(self, obj):
        """
        TBW
        """
        if isinstance(obj, list):
            # parse the given list of files
            input_file_paths = obj
            self.train_data = self._read_files(input_file_paths)
        else:
            # try loading from pickle
            input_file_path = obj
            self.train_data = pickle.load(io.open(input_file_path, "rb"))

    def dump_data(self, dump_file_path):
        """
        TBW
        """
        pickle.dump(self.train_data, io.open(dump_file_path, "wb"))

    def train(self, model_file_path):
        """
        TBW
        """
        # create a trainer object
        self.trainer = pycrfsuite.Trainer(verbose=self.verbose)

        # append training data
        for feature_seq, label_seq in self.train_data:
            self.trainer.append(feature_seq, label_seq)

        # do the actual training
        self.trainer.train(model_file_path)

        # return the path to the model file
        return model_file_path

    def trainer_info(self):
        if self.trainer is None:
            return None
        return self.trainer.info()


class CRFPredictor(object):
    """
    TBW
    """

    def __init__(self, model_file_path):
        self.model_file_path = model_file_path
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(self.model_file_path)

    @property
    def info(self):
        """
        TBW
        """
        if self.tagger is None:
            return None
        return self.tagger.info()

    def predict(self, obj):
        """
        TBW
        """
        features = None
        if isinstance(obj, list):
            features = obj
        elif isinstance(obj, Span):
            sentence = obj
            tokens = [token for token in sentence.elements if token.is_regular]
            features = tokens_to_features(tokens)
        else:
            raise TypeError(u"The obj should be either a Span (sentence) object or a list of features (dict) objects.")
        predicted_labels = self.tagger.tag(features)
        probability = self.tagger.probability(predicted_labels)
        return predicted_labels, probability


def usage(exit_code):
    """ Print usage and exit. """
    print(u"")
    print(u"Usage:")
    print(u"  $ python -m lachesis.ml.crf dump  LANGUAGE INPUT_DIR DUMP_FILE  [--small]")
    print(u"  $ python -m lachesis.ml.crf train LANGUAGE DUMP_FILE MODEL_FILE")
    print(u"  $ python -m lachesis.ml.crf test  LANGUAGE DUMP_FILE MODEL_FILE [--single]")
    print(u"")
    print(u"Options:")
    print(u"  --single : DUMP_FILE is a path to a single TTML file, not to a DUMP file created with dump")
    print(u"  --small  : only use first 10 TTML files from INPUT_DIR instead of all")
    print(u"")
    sys.exit(exit_code)


def main():
    """ Entry point. """

    def check_language(obj):
        """ Check that the given string identifies a known language. """
        language = Language.from_code(gf.to_unicode_string(obj))
        if language is None:
            print(u"[ERRO] Unknown language code '%s'" % obj)
            usage(1)
        return language

    def check_dir(obj):
        """ Check that the given string identifies an existing directory. """
        if not os.path.isdir(obj):
            print(u"[ERRO] Directory '%s' does not exist" % obj)
            usage(1)
        return obj

    def check_file(obj):
        """ Check that the given string identifies an existing file. """
        if not os.path.isfile(obj):
            print(u"[ERRO] File '%s' does not exist" % obj)
            usage(1)
        return obj

    def command_dump(language, input_directory_path, dump_file_path, small):
        """
        Create a cPickle dump with the features and labels
        from the TTML files contained in the given input directory.
        """
        input_files = []
        for root, dirs, files in os.walk(input_directory_path):
            input_files.extend([os.path.join(root, f) for f in files if f.endswith(u".ttml")])

        input_files = sorted(input_files)
        if small:
            input_files = input_files[:10]

        trainer = CRFTrainer(language=language)

        print(u"Parsing data...")
        trainer.load_data(input_files)
        print(u"Parsing data...done")

        print(u"Dumping data...")
        trainer.dump_data(dump_file_path)
        print(u"Dumping data... done")
        print(u"Dumped %d examples to: '%s'" % (len(trainer.train_data), dump_file_path))

    def command_train(language, dump_file_path, model_file_path):
        """
        Train a CRF model from the given dump file
        containing both features and labels.
        """
        print(u"Loading data...")
        trainer = CRFTrainer(language=language, nlpwrapper=u"pattern")
        trainer.load_data(dump_file_path)
        print(u"Loading data... done")

        print(u"Training...")
        trainer.train(model_file_path)
        print(u"Training... done")
        print(u"Built model '%s'" % model_file_path)

    def command_test(language, dump_file_path, model_file_path, single):
        """
        Test a CRF model against the given dump file
        containing both features and labels.

        The predictions are accounted for using
        the same algorithm powering the actual splitter.

        TBW
        """
        def check_prediction(l_predictor, l_subf, l_subl):
            """
            Call the tagger and check the prediction
            against the true value (i.e., the true label).
            """
            l_str = (u"".join([u"%s%s" % (f["word"], (u" " if f["ws"] else u"")) for f in l_subf])).strip()
            l_subl_pred, l_probability = l_predictor.predict(l_subf)
            l_pred_s = u"".join(l_subl_pred)
            l_real_s = u"".join(l_subl)
            return (l_real_s, l_pred_s, l_str, l_probability)

        def evaluate_predictions(all_predictions):
            """
            Explore all predictions for each CC line,
            choosing the prediction as the actual splitter does,
            and count the number of the splits correctly chosen.
            """
            cc_count = 0
            cc_count_good = 0
            for cc_prediction in all_predictions:
                cc_prediction_sorted = sorted(cc_prediction, key=lambda x: x[6], reverse=True)
                # for prefix_prediction in cc_prediction_sorted:
                #     print(prefix_prediction)
                # print(u"")
                cc_count += 1
                for pred in cc_prediction_sorted:
                    if pred[5] <= 42:
                        chosen = pred
                        break
                good = (not chosen[1]) and (chosen[3] == chosen[4]) and (chosen[3][-1] == CRFTrainer.LABEL_LAST)
                if good:
                    print("%s%s%s" % (ANSI_OK, chosen, ANSI_END))
                    cc_count_good += 1
                else:
                    print("%s%s%s" % (ANSI_ERROR, chosen, ANSI_END))
            return (cc_count, cc_count_good)

        print(u"Loading data...")
        trainer = CRFTrainer(language=language, nlpwrapper=u"pattern")
        arg = [dump_file_path] if single else dump_file_path
        trainer.load_data(arg)
        examples = trainer.train_data
        print(u"Loading data... done")

        print(u"Testing...")
        predictor = CRFPredictor(model_file_path)
        all_predictions = []
        n = len(examples)
        for idx in range(n):
            cc_predictions = []
            # test prefixes of the current line
            features, labels = examples[idx]
            for l in range(len(features)):
                subf = features[0:(l + 1)]
                subl = labels[0:(l + 1)]
                real_s, pred_s, str_s, prob = check_prediction(predictor, subf, subl)
                cc_predictions.append((idx, False, l, real_s, pred_s, len(str_s), prob))

            # test current line + prefixes of the next line
            # (if there is a next line)
            if idx + 1 < n:
                next_features, next_labels = examples[idx + 1]
                for l in range(len(next_features)):
                    subf = features + next_features[0:(l + 1)]
                    subl = labels + next_labels[0:(l + 1)]
                    real_s, pred_s, str_s, prob = check_prediction(predictor, subf, subl)
                    cc_predictions.append((idx, True, l, real_s, pred_s, len(str_s), prob))
            all_predictions.append(cc_predictions)
        print(u"Testing... done")

        print(u"Evaluating...")
        cc_count, cc_count_good = evaluate_predictions(all_predictions)
        print(u"Evaluating... done")
        print(u"CC lines segmented correctly: %d/%d (%.3f)" % (cc_count_good, cc_count, float(cc_count_good) / cc_count))

    ##########################################################################
    #
    # main script stats here
    #
    ##########################################################################
    if len(sys.argv) < 5:
        usage(1)

    command = sys.argv[1]
    small = u"--small" in sys.argv
    single = u"--single" in sys.argv

    if command not in [u"dump", u"train", u"test"]:
        print(u"[ERRO] Unknown command '%s'" % command)
        usage(1)

    if command == u"dump":
        language = check_language(sys.argv[2])
        input_directory_path = check_dir(sys.argv[3])
        dump_file_path = sys.argv[4]
        command_dump(language, input_directory_path, dump_file_path, small)

    if command == u"train":
        language = check_language(sys.argv[2])
        dump_file_path = check_file(sys.argv[3])
        model_file_path = sys.argv[4]
        command_train(language, dump_file_path, model_file_path)

    if command == u"test":
        language = check_language(sys.argv[2])
        dump_file_path = check_file(sys.argv[3])
        model_file_path = check_file(sys.argv[4])
        command_test(language, dump_file_path, model_file_path, single)

    sys.exit(0)


if __name__ == "__main__":
    main()
