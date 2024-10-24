import sys
import soundfile as sf
from jukebox.make_models import make_vqvae, make_prior
from jukebox.sample import sample_partial_window
import torch as t

def generate_music(artist, genre, lyrics, sample_length_in_seconds):
    vqvae, priors = make_vqvae(), [make_prior(level) for level in range(3)]
    
    z = t.zeros((1, 3, 8192))
    y = {
        'artist': artist,
        'genre': genre,
        'lyrics': lyrics,
        'sample_length_in_seconds': sample_length_in_seconds
    }

    # Generate the music
    sample = sample_partial_window(z, y, {
        'sample_length_in_seconds': sample_length_in_seconds,
        'levels': 3,
        'model_name': '5b',
        'n_ctx': 8192,
    }, vqvae, priors)

    # Save the music sample to a .wav file
    output_path = 'static/output_song.wav'
    sf.write(output_path, sample.cpu().numpy(), 44100)
    print("Music generated and saved at:", output_path)

if __name__ == "__main__":
    artist = sys.argv[1]
    genre = sys.argv[2]
    lyrics = sys.argv[3]
    sample_length_in_seconds = int(sys.argv[4])

    generate_music(artist, genre, lyrics, sample_length_in_seconds)
