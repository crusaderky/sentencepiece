# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.!

from collections import defaultdict
import io
import os
import pickle
import threading

import pytest

import sentencepiece as spm

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(DATA_DIR, "test_model.model")
MODEL_JA_FILE = os.path.join(DATA_DIR, "test_ja_model.model")
BOTCHAN = os.path.join(DATA_DIR, "botchan.txt")


class TestSentencepieceProcessor:
    """Test case for SentencePieceProcessor"""

    def setup_method(self):
        self.sp_ = spm.SentencePieceProcessor()
        self.jasp_ = spm.SentencePieceProcessor()
        assert self.sp_.Load(MODEL_FILE)
        assert self.jasp_.Load(MODEL_JA_FILE)
        with open(MODEL_FILE, "rb") as f:
            assert self.sp_.LoadFromSerializedProto(f.read())
        with open(MODEL_JA_FILE, "rb") as f:
            assert self.jasp_.LoadFromSerializedProto(f.read())

    def test_load(self):
        assert self.sp_.GetPieceSize() == 1000
        assert self.sp_.PieceToId("<unk>") == 0
        assert self.sp_.PieceToId("<s>") == 1
        assert self.sp_.PieceToId("</s>") == 2
        assert self.sp_.IdToPiece(0) == "<unk>"
        assert self.sp_.IdToPiece(1) == "<s>"
        assert self.sp_.IdToPiece(2) == "</s>"
        assert self.sp_.unk_id() == 0
        assert self.sp_.bos_id() == 1
        assert self.sp_.eos_id() == 2
        assert self.sp_.pad_id() == -1
        for i in range(self.sp_.GetPieceSize()):
            piece = self.sp_.IdToPiece(i)
            assert self.sp_.PieceToId(piece) == i

        assert self.sp_.get_piece_size() == 1000
        assert self.sp_.piece_to_id("<unk>") == 0
        assert self.sp_.piece_to_id("<s>") == 1
        assert self.sp_.piece_to_id("</s>") == 2
        assert self.sp_.id_to_piece(0) == "<unk>"
        assert self.sp_.id_to_piece(1) == "<s>"
        assert self.sp_.id_to_piece(2) == "</s>"
        for i in range(self.sp_.get_piece_size()):
            piece = self.sp_.id_to_piece(i)
            assert self.sp_.piece_to_id(piece) == i

    def test_roundtrip(self):
        text = "I saw a girl with a telescope."
        ids = self.sp_.EncodeAsIds(text)
        pieces1 = self.sp_.EncodeAsPieces(text)
        pieces2 = self.sp_.NBestEncodeAsPieces(text, 10)[0]
        assert pieces1 == pieces2
        assert self.sp_.DecodePieces(pieces1) == text
        assert self.sp_.DecodeIds(ids) == text
        for _ in range(100):
            assert (
                self.sp_.DecodePieces(self.sp_.SampleEncodeAsPieces(text, 64, 0.5))
                == text
            )
            assert (
                self.sp_.DecodePieces(self.sp_.SampleEncodeAsPieces(text, -1, 0.5))
                == text
            )
            assert self.sp_.DecodeIds(self.sp_.SampleEncodeAsIds(text, 64, 0.5)) == text
            assert self.sp_.DecodeIds(self.sp_.SampleEncodeAsIds(text, -1, 0.5)) == text

        ids2 = self.sp_.encode_as_ids(text)
        pieces3 = self.sp_.encode_as_pieces(text)
        pieces4 = self.sp_.nbest_encode_as_pieces(text, 10)[0]
        assert pieces3 == pieces4
        assert pieces3 == pieces1
        assert ids2 == ids
        assert self.sp_.decode_pieces(pieces3) == text
        assert self.sp_.decode_ids(ids2) == text
        for _ in range(100):
            assert (
                self.sp_.decode_pieces(self.sp_.sample_encode_as_pieces(text, 64, 0.5))
                == text
            )
            assert (
                self.sp_.decode_pieces(self.sp_.sample_encode_as_pieces(text, -1, 0.5))
                == text
            )
            assert (
                self.sp_.decode_ids(self.sp_.sample_encode_as_ids(text, 64, 0.5))
                == text
            )
            assert (
                self.sp_.decode_ids(self.sp_.sample_encode_as_ids(text, -1, 0.5))
                == text
            )

        assert self.sp_.calculate_entropy(text, 0.1) == self.sp_.CalculateEntropy(
            text, 0.1
        )

    def test_ja_load(self):
        assert self.jasp_.GetPieceSize() == 8000
        assert self.jasp_.PieceToId("<unk>") == 0
        assert self.jasp_.PieceToId("<s>") == 1
        assert self.jasp_.PieceToId("</s>") == 2
        assert self.jasp_.IdToPiece(0) == "<unk>"
        assert self.jasp_.IdToPiece(1) == "<s>"
        assert self.jasp_.IdToPiece(2) == "</s>"
        for i in range(self.jasp_.GetPieceSize()):
            piece = self.jasp_.IdToPiece(i)
            assert self.jasp_.PieceToId(piece) == i

        assert self.jasp_.get_piece_size() == 8000
        assert self.jasp_.piece_to_id("<unk>") == 0
        assert self.jasp_.piece_to_id("<s>") == 1
        assert self.jasp_.piece_to_id("</s>") == 2
        assert self.jasp_.id_to_piece(0) == "<unk>"
        assert self.jasp_.id_to_piece(1) == "<s>"
        assert self.jasp_.id_to_piece(2) == "</s>"
        for i in range(self.jasp_.get_piece_size()):
            piece = self.jasp_.id_to_piece(i)
            assert self.jasp_.piece_to_id(piece) == i

    def test_ja_roundtrip(self):
        text = "清水寺は京都にある。"
        ids = self.jasp_.EncodeAsIds(text)
        pieces1 = self.jasp_.EncodeAsPieces(text)
        pieces2 = self.jasp_.NBestEncodeAsPieces(text, 10)[0]
        assert pieces1 == pieces2
        assert self.jasp_.DecodePieces(pieces1) == text
        assert self.jasp_.DecodeIds(ids) == text
        for _ in range(100):
            assert (
                self.jasp_.DecodePieces(self.jasp_.SampleEncodeAsPieces(text, 64, 0.5))
                == text
            )
            assert (
                self.jasp_.DecodePieces(self.jasp_.SampleEncodeAsPieces(text, -1, 0.5))
                == text
            )

        ids2 = self.jasp_.encode_as_ids(text)
        pieces3 = self.jasp_.encode_as_pieces(text)
        pieces4 = self.jasp_.nbest_encode_as_pieces(text, 10)[0]
        assert pieces4 == pieces3
        assert pieces3 == pieces1
        assert ids2 == ids
        assert self.jasp_.decode_pieces(pieces1) == text
        assert self.jasp_.decode_ids(ids2) == text
        for _ in range(100):
            assert (
                self.jasp_.decode_pieces(
                    self.jasp_.sample_encode_as_pieces(text, 64, 0.5)
                )
                == text
            )
            assert (
                self.jasp_.decode_pieces(
                    self.jasp_.sample_encode_as_pieces(text, -1, 0.5)
                )
                == text
            )
            assert self.jasp_.CalculateEntropy(
                text, 0.1
            ) == self.jasp_.calculate_entropy(text, 0.1)

    def test_train(self, tmp_path):
        tid = threading.get_ident()
        model_prefix = f"{tmp_path}/m_{tid}"

        spm.SentencePieceTrainer.Train(
            f"--input={BOTCHAN} --model_prefix={model_prefix} --vocab_size=1000"
        )
        sp = spm.SentencePieceProcessor()
        sp.Load(f"{model_prefix}.model")
        with open(BOTCHAN, "r") as file:
            for line in file:
                sp.DecodePieces(sp.EncodeAsPieces(line))
                sp.DecodeIds(sp.EncodeAsIds(line))

    def test_train_iterator(self, tmp_path):
        tid = threading.get_ident()
        model_prefix = f"{tmp_path}/m_{tid}"

        spm.SentencePieceTrainer.Train(
            f"--input={BOTCHAN} --model_prefix={model_prefix} --vocab_size=1000"
        )
        os1 = io.BytesIO()
        os2 = io.BytesIO()

        # suppress logging (redirect to /dev/null)
        spm.SentencePieceTrainer.train(
            input=BOTCHAN,
            model_prefix=model_prefix,
            vocab_size=1000,
            logstream=open(os.devnull, "w"),
        )

        with open(BOTCHAN, "rb") as is1:
            spm.SentencePieceTrainer.train(
                sentence_iterator=is1,
                model_prefix=model_prefix,
                vocab_size=1000,
                logstream=open(os.devnull, "w"),
            )

        spm.SentencePieceTrainer.train(
            input=BOTCHAN,
            model_writer=os1,
            vocab_size=1000,
            logstream=open(os.devnull, "w"),
        )

        with open(BOTCHAN, "rb") as is2:
            spm.SentencePieceTrainer.train(
                sentence_iterator=is2,
                model_writer=os2,
                vocab_size=1000,
                logstream=open(os.devnull, "w"),
            )

        sp1 = spm.SentencePieceProcessor(model_proto=os1.getvalue())
        sp2 = spm.SentencePieceProcessor(model_proto=os2.getvalue())
        assert [sp1.id_to_piece(i) for i in range(sp1.get_piece_size())] == [
            sp2.id_to_piece(i) for i in range(sp2.get_piece_size())
        ]

    def test_train_kwargs(self, tmp_path):
        tid = threading.get_ident()
        model_prefix = f"{tmp_path}/m_{tid}"

        # suppress logging (redirect to /dev/null)
        spm.SentencePieceTrainer.train(
            input=[BOTCHAN],
            model_prefix=model_prefix,
            vocab_size=1002,
            user_defined_symbols=["foo", "bar", ",", " ", "\t", "\b", "\n", "\r"],
            logstream=open(os.devnull, "w"),
        )
        sp = spm.SentencePieceProcessor()
        sp.Load(f"{model_prefix}.model")
        with open(BOTCHAN, "r") as file:
            for line in file:
                sp.DecodePieces(sp.EncodeAsPieces(line))
                sp.DecodeIds(sp.EncodeAsIds(line))

        s = "hello\tworld\r\nthis\tis a \b pen"
        assert sp.decode(sp.encode(s)) == s

    def test_serialized_proto(self):
        text = "I saw a girl with a telescope."
        s1 = self.sp_.EncodeAsSerializedProto(text)
        s2 = self.sp_.SampleEncodeAsSerializedProto(text, 10, 0.2)
        s3 = self.sp_.NBestEncodeAsSerializedProto(text, 10)
        s4 = self.sp_.DecodePiecesAsSerializedProto(["foo", "bar"])
        s5 = self.sp_.DecodeIdsAsSerializedProto([20, 30])

        t1 = self.sp_.encode_as_serialized_proto(text)
        t2 = self.sp_.sample_encode_as_serialized_proto(text, 10, 0.2)
        t3 = self.sp_.nbest_encode_as_serialized_proto(text, 10)
        t4 = self.sp_.decode_pieces_as_serialized_proto(["foo", "bar"])
        t5 = self.sp_.decode_ids_as_serialized_proto([20, 30])

        y1 = self.sp_.encode(text, out_type="serialized_proto")
        y2 = self.sp_.encode(text, enable_sampling=True, out_type="serialized_proto")
        y3 = self.sp_.nbest_encode(text, out_type="serialized_proto", nbest_size=10)
        y4 = self.sp_.decode(["foo", "bar"], out_type="serialized_proto")
        y5 = self.sp_.decode([20, 30], out_type="serialized_proto")
        assert isinstance(s1, bytes)
        assert isinstance(s2, bytes)
        assert isinstance(t2, bytes)
        assert isinstance(s3, bytes)
        assert isinstance(s4, bytes)
        assert isinstance(s5, bytes)

        assert s1 == t1
        assert s3 == t3
        assert s4 == t4
        assert s5 == t5
        assert s1 == y1
        assert s3 == y3
        assert s4 == y4
        assert s5 == y5

        ids = self.jasp_.EncodeAsIds(text)
        pieces = self.jasp_.EncodeAsPieces(text)
        s1 = self.jasp_.EncodeAsSerializedProto(text)
        s2 = self.jasp_.DecodeIdsAsSerializedProto(ids)
        s3 = self.jasp_.DecodePiecesAsSerializedProto(ids)
        assert s2 == s1
        assert s3 == s1

    def test_decode_bytes(self):
        texts = ["Hello world", "清水寺は京都にある。"]
        ids = self.jasp_.encode(texts, out_type=int)
        s1 = self.jasp_.decode(ids, out_type=bytes)
        s2 = self.jasp_.decode(ids, out_type=str)
        assert len(s1) == 2
        assert isinstance(s1[0], bytes)
        assert isinstance(s1[1], bytes)
        assert len(s2) == 2
        assert isinstance(s2[0], str)
        assert isinstance(s2[1], str)
        assert s1[0].decode(encoding="utf-8") == s2[0]
        assert s1[1].decode(encoding="utf-8") == s2[1]

        text = "Hello world"
        ids = self.jasp_.encode(text, out_type=int)
        s1 = self.jasp_.decode(ids, out_type=bytes)
        s2 = self.jasp_.decode(ids, out_type=str)
        assert isinstance(s1, bytes)
        assert isinstance(s2, str)
        assert s1.decode(encoding="utf-8") == s2

        x = self.jasp_.encode(text, out_type="immutable_proto")
        assert x.text_as_bytes.decode(encoding="utf-8") == x.text
        for sp in x.pieces:
            assert sp.piece_as_bytes.decode(encoding="utf-8") == sp.piece
            assert sp.surface_as_bytes.decode(encoding="utf-8") == sp.surface

        x = self.jasp_.decode(ids, out_type="immutable_proto")
        assert x.text_as_bytes.decode(encoding="utf-8") == x.text
        for sp in x.pieces:
            assert sp.piece_as_bytes.decode(encoding="utf-8") == sp.piece
            assert sp.surface_as_bytes.decode(encoding="utf-8") == sp.surface

    def test_immutable_proto(self):
        text = "I saw a girl with a telescope."
        s1 = self.sp_.EncodeAsImmutableProto(text)
        s2 = self.sp_.SampleEncodeAsImmutableProto(text, 10, 0.2)
        s3 = self.sp_.NBestEncodeAsImmutableProto(text, 10)
        s4 = self.sp_.DecodePiecesAsImmutableProto(["foo", "bar"])
        s5 = self.sp_.DecodeIdsAsImmutableProto([20, 30])

        t1 = self.sp_.encode_as_immutable_proto(text)
        t2 = self.sp_.sample_encode_as_immutable_proto(text, 10, 0.2)
        t3 = self.sp_.nbest_encode_as_immutable_proto(text, 10)
        t4 = self.sp_.decode_pieces_as_immutable_proto(["foo", "bar"])
        t5 = self.sp_.decode_ids_as_immutable_proto([20, 30])

        y1 = self.sp_.encode(text, out_type="immutable_proto")
        y2 = self.sp_.encode(text, enable_sampling=True, out_type="immutable_proto")
        y3 = self.sp_.nbest_encode(text, out_type="immutable_proto", nbest_size=10)
        y4 = self.sp_.decode(["foo", "bar"], out_type="immutable_proto")
        y5 = self.sp_.decode([20, 30], out_type="immutable_proto")

        assert s1 == t1
        assert s3 == t3
        assert s4 == t4
        assert s5 == t5
        assert s1 == y1
        assert s3 == y3
        assert s4 == y4
        assert s5 == y5

        hset_piece = defaultdict(int)

        # eq test
        for i in range(len(s1.pieces)):
            assert s1.pieces[i] == t1.pieces[i]
            hset_piece[s1.pieces[i]] += 1
            hset_piece[t1.pieces[i]] += 1

        assert len(s1.pieces) == len(hset_piece)

        # has test
        hset = defaultdict(int)
        hset[s1] += 1
        hset[t1] += 1
        hset[s3] += 1
        hset[t3] += 1

        assert len(hset) == 2
        assert hset[s1] == 2
        assert hset[s3] == 2
        assert hset[t1] == 2
        assert hset[t3] == 2

        x1 = self.sp_.encode_as_serialized_proto(text)
        x2 = self.sp_.sample_encode_as_serialized_proto(text, 10, 0.2)
        x3 = self.sp_.nbest_encode_as_serialized_proto(text, 10)
        x4 = self.sp_.decode_pieces_as_serialized_proto(["foo", "bar"])
        x5 = self.sp_.decode_ids_as_serialized_proto([20, 30])

        assert x1 == t1.SerializeAsString()
        assert x3 == t3.SerializeAsString()
        assert x4 == t4.SerializeAsString()
        assert x5 == t5.SerializeAsString()

        v1 = self.sp_.EncodeAsIds(text)
        v2 = self.sp_.EncodeAsPieces(text)
        assert [x.id for x in s1.pieces] == v1
        assert [x.piece for x in s1.pieces] == v2
        assert s1.text == text

        surfaces1 = [s1.text[x.begin : x.end] for x in s1.pieces]
        surfaces2 = [x.surface for x in s1.pieces]
        assert surfaces1 == surfaces2

        ids = []
        for i in range(len(s1.pieces)):
            ids.append(s1.pieces[i].id)
        assert ids == v1

        pieces = []
        for i in range(len(s1.pieces)):
            pieces.append(s1.pieces[i].piece)
        assert pieces == v2

        for v in s3.nbests:
            assert v.text == text
            assert self.sp_.Decode([x.id for x in v.pieces]) == text

        for i in range(len(s3.nbests)):
            assert s3.nbests[i].text == text
            assert self.sp_.Decode([x.id for x in s3.nbests[i].pieces]) == text

        # slice
        assert s1.pieces[::-1] == list(reversed(s1.pieces))
        assert s3.nbests[::-1] == list(reversed(s3.nbests))

        # Japanese offset
        s1 = self.jasp_.EncodeAsImmutableProto("吾輩は猫である。Hello world. ABC 123")
        surfaces1 = [s1.text[x.begin : x.end] for x in s1.pieces]
        surfaces2 = [x.surface for x in s1.pieces]
        assert surfaces1 == surfaces2

        ids = [x.id for x in s1.pieces]
        s2 = self.jasp_.DecodeIdsAsImmutableProto(ids)
        assert s2 == s1

        pieces = [x.piece for x in s1.pieces]
        s2 = self.jasp_.DecodePiecesAsImmutableProto(pieces)
        assert s2 == s1

    def test_new_api(self):
        sp = spm.SentencePieceProcessor(model_file=MODEL_FILE)
        text = "hello world"
        text2 = "Tokyo"
        ids = self.sp_.EncodeAsIds(text)
        ids2 = self.sp_.EncodeAsIds(text2)
        pieces = self.sp_.EncodeAsPieces(text)
        pieces2 = self.sp_.EncodeAsPieces(text2)
        sprotos = self.sp_.EncodeAsSerializedProto(text)
        sproto2 = self.sp_.EncodeAsSerializedProto(text2)
        iprotos = self.sp_.EncodeAsImmutableProto(text)
        iprotos2 = self.sp_.EncodeAsImmutableProto(text2)

        assert sp.encode(text, out_type=int) == ids
        assert sp.encode(text, out_type=str) == pieces
        assert sp.encode(text, out_type="serialized_proto") == sprotos
        assert sp.encode(text, out_type="immutable_proto") == iprotos

        assert sp.encode([text], out_type=int) == [ids]
        assert sp.encode([text], out_type=str) == [pieces]
        assert sp.encode([text], out_type="serialized_proto") == [sprotos]
        assert sp.encode([text], out_type="immutable_proto") == [iprotos]

        assert len(iprotos.pieces) == len(pieces)
        assert len(iprotos.pieces) == len(ids)
        assert iprotos.text == text

        assert len(iprotos2.pieces) == len(pieces2)
        assert len(iprotos2.pieces) == len(ids2)
        assert iprotos2.text == text2

        for i in range(len(iprotos.pieces)):
            assert ids[i] == iprotos.pieces[i].id
            assert pieces[i] == iprotos.pieces[i].piece

        for i, piece in enumerate(iprotos.pieces):
            assert ids[i] == piece.id
            assert pieces[i] == piece.piece

        for i in range(len(iprotos2.pieces)):
            assert ids2[i] == iprotos2.pieces[i].id
            assert pieces2[i] == iprotos2.pieces[i].piece

        for i, piece in enumerate(iprotos2.pieces):
            assert ids2[i] == piece.id
            assert pieces2[i] == piece.piece

        detok_ids = self.sp_.DecodeIds(ids)
        detok_pieces = self.sp_.DecodePieces(pieces)
        assert sp.decode(ids) == detok_ids
        assert sp.decode(pieces) == detok_pieces
        assert sp.decode([]) == ""
        assert sp.decode([[]]) == [""]

        # add_bos, add_eos, reverse
        assert [sp.bos_id()] + ids == sp.encode(text, add_bos=True)
        assert ids + [sp.eos_id()] == sp.encode(text, add_eos=True)
        assert ids + [sp.eos_id()] == sp.EncodeAsIds(text, add_eos=True)
        rids = ids[:]
        rids.reverse()

        assert rids == sp.encode(text, reverse=True)
        assert rids == sp.EncodeAsIds(text, reverse=True)

        # different shape.
        assert [ids, ids2] == sp.encode([text, text2])
        assert [pieces, pieces2] == sp.encode([text, text2], out_type=str)
        assert [text, text2] == sp.decode([ids, ids2])
        assert [text, text2] == sp.decode([pieces, pieces2])

        pieces = list(reversed(self.sp_.EncodeAsPieces(text)))
        assert pieces == sp.encode(text, reverse=True, out_type=str)

        # emit unk piece
        unk_char = "藤"
        pieces = self.sp_.EncodeAsIds(unk_char, emit_unk_piece=True)
        pieces2 = self.sp_.encode(unk_char, out_type=int, emit_unk_piece=True)
        assert pieces[1] == sp.unk_id()
        assert pieces2[1] == sp.unk_id()
        assert pieces == pieces2

        pieces = self.sp_.EncodeAsPieces(unk_char, emit_unk_piece=True)
        pieces2 = self.sp_.encode(unk_char, out_type=str, emit_unk_piece=True)
        assert pieces[1] == "<unk>"
        assert pieces2[1] == "<unk>"
        assert pieces == pieces2

        pieces = self.sp_.EncodeAsPieces(unk_char, emit_unk_piece=False)
        pieces2 = self.sp_.encode(unk_char, out_type=str, emit_unk_piece=False)
        assert pieces[1] == unk_char
        assert pieces2[1] == unk_char
        assert pieces == pieces2

    def test_new_api_init(self):
        sp = spm.SentencePieceProcessor(
            model_file=MODEL_FILE,
            add_bos=True,
            add_eos=True,
            out_type=str,
        )
        text = "hello world"
        pieces = ["<s>"] + self.sp_.EncodeAsPieces(text) + ["</s>"]
        assert pieces == sp.encode(text)

        pieces = self.sp_.EncodeAsPieces(text) + ["</s>"]
        assert pieces == sp.encode(text, add_bos=False, add_eos=True)

    def test_sampling(self):
        sp = self.sp_

        for out_type in [str, int, "serialized_proto", "immutable_proto"]:
            ids = defaultdict(int)
            for _ in range(100):
                out = sp.encode("hello world", out_type=out_type, enable_sampling=True)
                if type(out) is list:
                    out = tuple(out)
                ids[out] += 1
            assert len(ids) > 1

            ids2 = defaultdict(int)
            for _ in range(100):
                out = sp.encode("hello world", out_type=out_type, enable_sampling=False)
                if type(out) is list:
                    out = tuple(out)
                ids2[out] += 1
            assert len(ids2) == 1

            out = sp.encode(
                ["hello world", "this is a test"],
                out_type=out_type,
                enable_sampling=True,
            )
            assert len(out) == 2
            out = sp.encode(
                ["hello world", "this is a test"],
                out_type=out_type,
                enable_sampling=False,
            )
            assert len(out) == 2

    def test_nbest(self):
        sp = self.sp_
        text = "hello world"
        text2 = "I have a pen."

        for out_type in [str, int, "serialized_proto", "immutable_proto"]:
            results = sp.nbest_encode(text, nbest_size=10, out_type=out_type)
            assert results == sp.NBestEncode(text, nbest_size=10, out_type=out_type)

            if out_type in [str, int]:
                for n in results:
                    assert sp.decode(n) == text

                for n in sp.decode(results):
                    assert n == text

            # batch test
            results = sp.nbest_encode([text, text2], nbest_size=10, out_type=out_type)
            assert results == sp.NBestEncode(
                [text, text2], nbest_size=10, out_type=out_type
            )
            assert len(results) == 2

            if out_type in [str, int]:
                for n in results[0]:
                    assert sp.decode(n) == text

                for n in results[1]:
                    assert sp.decode(n) == text2

                decoded = sp.decode(results[0])
                assert len(decoded) == 10
                for n in decoded:
                    assert n == text
                decoded = sp.decode(results[1])
                assert len(decoded) == 10
                for n in decoded:
                    assert n == text2

                assert sp.nbest_encode(
                    text, nbest_size=10, out_type=str
                ) == sp.nbest_encode_as_pieces(text, nbest_size=10)
                assert sp.nbest_encode(
                    text, nbest_size=10, out_type=int
                ) == sp.nbest_encode_as_ids(text, nbest_size=10)
                assert sp.nbest_encode(
                    text, nbest_size=10, out_type="serialized_proto"
                ) == sp.nbest_encode_as_serialized_proto(text, nbest_size=10)
                assert sp.nbest_encode(
                    text, nbest_size=10, out_type="immutable_proto"
                ) == sp.nbest_encode_as_immutable_proto(text, nbest_size=10)

    def test_sample_and_score(self):
        sp = self.sp_
        text = "hello world"
        text2 = "I have a pen."
        for out_type in [str, int, "serialized_proto", "immutable_proto"]:
            results = sp.sample_encode_and_score(
                text, wor=True, num_samples=10, out_type=out_type
            )
            results = sp.SampleEncodeAndScore(
                text, wor=False, num_samples=10, out_type=out_type
            )

            if out_type in [str, int]:
                for n in results:
                    assert sp.decode(n[0]) == text

            results = sp.sample_encode_and_score(
                [text, text2], wor=True, num_samples=10, out_type=out_type
            )
            results = sp.SampleEncodeAndScore(
                [text, text2], wor=True, num_samples=10, out_type=out_type
            )

            if out_type in [str, int]:
                for n in results[0]:
                    assert sp.decode(n[0]) == text
                for n in results[1]:
                    assert sp.decode(n[0]) == text2

        sp.sample_encode_and_score_as_pieces(text, 10)
        sp.sample_encode_and_score_as_ids(text, 10)
        sp.sample_encode_and_score_as_immutable_proto(text, 10)
        sp.sample_encode_and_score_as_serialized_proto(text, 10)

    @pytest.mark.parametrize(
        "meth_name",
        [
            "IdToPiece",
            "GetScore",
            "IsUnknown",
            "IsControl",
            "IsUnused",
            "IsByte",
            "DecodeIds",
            "DecodeIdsAsSerializedProto",
        ],
    )
    def test_valid_range(self, meth_name):
        size = self.sp_.piece_size()
        meth = getattr(self.sp_, meth_name)
        meth([10, 20, 30])
        try:
            meth([size])
        except IndexError:
            pass

    def test_batch(self):
        sp = spm.SentencePieceProcessor(model_file=MODEL_FILE)
        with open(BOTCHAN, "r") as file:
            texts = file.readlines()

        for out_type in [str, int, "serialized_proto", "immutable_proto"]:
            r1 = sp.encode(texts, out_type=out_type, num_threads=None)
            r2 = sp.encode(texts, out_type=out_type, num_threads=1)
            r3 = sp.encode(texts, out_type=out_type, num_threads=-1)
            r4 = sp.encode(texts, out_type=out_type, num_threads=8)
            r5 = [sp.encode(s, out_type=out_type) for s in texts]
            assert r2 == r1
            assert r3 == r1
            assert r4 == r1
            assert r5 == r1

            if out_type in [str, int]:
                d1 = sp.decode(r1, num_threads=None)
                d2 = sp.decode(r2, num_threads=1)
                d3 = sp.decode(r3, num_threads=-1)
                d4 = sp.decode(r4, num_threads=8)
                d5 = [sp.decode(s) for s in r5]

                assert d2 == d1
                assert d3 == d1
                assert d4 == d1
                assert d5 == d1

        e1 = sp.calculate_entropy(texts, alpha=1.0, num_threads=10)
        e2 = sp.CalculateEntropy(texts, alpha=1.0, num_threads=10)
        e3 = [sp.calculate_entropy(s, alpha=1.0) for s in texts]
        assert e2 == e1
        assert e3 == e1

    def test_pickle(self):
        pik = pickle.dumps(self.sp_)
        id1 = self.sp_.encode("hello world.", out_type=int)
        sp = pickle.loads(pik)
        id2 = sp.encode("hello world.", out_type=int)
        assert id2 == id1

    def test_global_params(self):
        spm.SetRandomGeneratorSeed(0)
        spm.SetMinLogLevel(2)
        spm.set_random_generator_seed(1)
        spm.set_min_log_level(3)

    def test_normalize(self):
        sp = spm.SentencePieceProcessor(model_file=MODEL_FILE)
        assert sp.normalize("ＫＡＤＯＫＡＷＡABC") == "▁KADOKAWAABC"
        assert sp.Normalize("ＫＡＤＯＫＡＷＡABC") == "▁KADOKAWAABC"

        x = sp.Normalize("ＫＡＤＯＫＡＷＡABC", with_offsets=True)
        assert x[0] == "▁KADOKAWAABC"
        assert x[1] == [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        x = sp.Normalize("ＫＡＤＯＫＡＷＡABC".encode("utf8"), with_offsets=True)
        assert x[0] == "▁KADOKAWAABC".encode("utf8")
        assert x[1] == [0, 0, 0, 0, 3, 6, 9, 12, 15, 18, 21, 24, 25, 26, 27]

        assert sp.normalize(["ＫＡＤＯＫＡＷＡABC", "㍻"]) == ["▁KADOKAWAABC", "▁平成"]
        assert sp.Normalize(["ＫＡＤＯＫＡＷＡABC", "㍻"]) == ["▁KADOKAWAABC", "▁平成"]

        x = sp.Normalize(
            ["ＫＡＤＯＫＡＷＡABC".encode("utf8"), "㍻".encode("utf8")],
            with_offsets=True,
        )
        assert len(x) == 2
        assert x[0][0] == "▁KADOKAWAABC".encode("utf8")
        assert x[0][1] == [0, 0, 0, 0, 3, 6, 9, 12, 15, 18, 21, 24, 25, 26, 27]

        x = sp.Normalize(["ＫＡＤＯＫＡＷＡABC", "㍻"], with_offsets=True)
        assert len(x) == 2
        assert x[0][0] == "▁KADOKAWAABC"
        assert x[0][1] == [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        assert x[1][0] == "▁平成"
        assert x[1][1] == [0, 0, 0, 1]

    def test_normalizer(self):
        sp = spm.SentencePieceNormalizer(model_file=MODEL_FILE)

        assert sp.normalize("ＫＡＤＯＫＡＷＡABC") == "KADOKAWAABC"
        assert sp.Normalize("ＫＡＤＯＫＡＷＡABC") == "KADOKAWAABC"

        x = sp.Normalize("ＫＡＤＯＫＡＷＡABC".encode("utf8"), with_offsets=True)
        assert x[0] == "KADOKAWAABC".encode("utf8")
        assert x[1] == [0, 3, 6, 9, 12, 15, 18, 21, 24, 25, 26, 27]

        x = sp.Normalize("ＫＡＤＯＫＡＷＡABC", with_offsets=True)
        assert x[0] == "KADOKAWAABC"
        assert x[1] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        assert sp.normalize(["ＫＡＤＯＫＡＷＡABC", "㍻"]) == ["KADOKAWAABC", "平成"]
        assert sp.Normalize(["ＫＡＤＯＫＡＷＡABC", "㍻"]) == ["KADOKAWAABC", "平成"]

        x = sp.Normalize(
            ["ＫＡＤＯＫＡＷＡABC".encode("utf8"), "㍻".encode("utf8")],
            with_offsets=True,
        )
        assert len(x) == 2
        assert x[0][0] == "KADOKAWAABC".encode("utf8")
        assert x[0][1] == [0, 3, 6, 9, 12, 15, 18, 21, 24, 25, 26, 27]

        x = sp.Normalize(["ＫＡＤＯＫＡＷＡABC", "㍻"], with_offsets=True)
        assert len(x) == 2
        assert x[0][0] == "KADOKAWAABC"
        assert x[0][1] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        assert x[1][0] == "平成"
        assert x[1][1] == [0, 0, 1]

        sp = spm.SentencePieceNormalizer(
            model_file=MODEL_FILE,
            add_dummy_prefix=True,
            escape_whitespaces=True,
            remove_extra_whitespaces=False,
        )
        assert sp.normalize("hello  world") == "▁hello▁▁world"

        sp = spm.SentencePieceNormalizer(
            model_file=MODEL_FILE,
            add_dummy_prefix=True,
            escape_whitespaces=True,
            remove_extra_whitespaces=True,
        )
        assert sp.normalize("  hello  world  ") == "▁hello▁world"

        sp = spm.SentencePieceNormalizer(
            model_file=MODEL_FILE,
            add_dummy_prefix=False,
            escape_whitespaces=False,
            remove_extra_whitespaces=True,
        )
        assert sp.normalize("  hello  world  ") == "hello world"

    def test_normalizer_rule(self):
        sp = spm.SentencePieceNormalizer(rule_name="identity")
        assert sp.Normalize("ＡＢＣ") == "ＡＢＣ"

        sp = spm.SentencePieceNormalizer(rule_name="nfkc_cf")
        assert sp.Normalize("ＡＢＣ") == "abc"

    def test_override_normalize_spec(self):
        sp = spm.SentencePieceProcessor(model_file=MODEL_FILE)

        expect = ["▁he", "ll", "o", "▁world"]
        assert sp.EncodeAsPieces(" hello  world ") == expect

        sp.override_normalizer_spec(add_dummy_prefix=False)
        sp.override_normalizer_spec(remove_extra_whitespaces=False)
        sp.override_normalizer_spec(escape_whitespaces=False)

        expect = [" ", "he", "ll", "o", "  ", "w", "or", "l", "d", " "]
        assert sp.EncodeAsPieces(" hello  world ") == expect
