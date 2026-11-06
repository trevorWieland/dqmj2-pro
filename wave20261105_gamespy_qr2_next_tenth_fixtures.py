import wave20261105_gamespy_qr2_next_first_fixtures as H
import wave20261105_gamespy_qr2_next_tenth_models as F


def run(image,row,body,v,seed):
    previous=H.F
    try:H.F=F;return H.run(image,row,body,v,seed)
    finally:H.F=previous


def prove(row,native,source):
    previous=H.F
    try:H.F=F;return H.prove(row,native,source)
    finally:H.F=previous
