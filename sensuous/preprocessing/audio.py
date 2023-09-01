import os
import numpy as np
import cv2
import librosa
from skimage.io import imsave
from skimage.transform import resize
import sensuous.parameters as params


def convert_audios_to_spectrograms(mp3_dir, png_dir):
    """Convert all mp3 files in mp3_dir to spectrograms and save them
    as png files to png_dir"""
    for mp3_file in os.listdir(mp3_dir):
        if mp3_file.endswith(".mp3"):

            # Convert the mp3 file into a spectrogram
            spec = mp3_to_spectrogram(os.path.join(mp3_dir, mp3_file))

            # Save the spectrogram as an image file
            output_file = os.path.join(png_dir,
                                       os.path.splitext(mp3_file)[0] + ".png")

            # imsave(output_file, spec)
            imsave(output_file, (spec).astype(np.uint8))


def mp3_to_spectrogram(mp3_file):
    """Converts a single mp3 file to a png spectrogram"""
    # Load the mp3 file
    y, sr = librosa.load(mp3_file)

    # Calculate the Mel spectrogram
    spec = librosa.stft(y)
    spec_mag, _ = librosa.magphase(spec)
    mel_spec = librosa.feature.melspectrogram(S=spec_mag, sr=sr)
    spec_db = librosa.amplitude_to_db(abs(mel_spec))

    # Resize the spectrogram
    spec_resized = resize(spec_db, (128, 128))
    spec_resized = cv2.normalize(spec_resized, None, 255, 0, cv2.NORM_MINMAX,
                                 cv2.CV_8U)

    return spec_resized


if __name__ == "__main__":
    mp3_dir = params.LOCAL_MP3_DIR
    png_dir = params.LOCAL_PNG_DIR
    convert_audios_to_spectrograms(mp3_dir, png_dir)
    print('mp3 files successfully converted to png spectrograms.')
