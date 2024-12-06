import numpy as np

class FFTTransform:
    @staticmethod
    def compress_message(message, compression_level):
        """
        Compresses the message using FFT with a specified compression level.
        
        Args:
            message (str): The message to compress.
            compression_level (int): Number of FFT coefficients to retain.

        Returns:
            tuple: Compressed message (str) and the transformed coefficients (array).
        """
        # Convert the message into a numeric representation
        numeric_message = np.array([ord(c) for c in message], dtype=np.float64)
        
        # Apply FFT
        transformed_message = np.fft.fft(numeric_message)
        
        # Retain only the top `compression_level` coefficients
        compressed_message = np.zeros_like(transformed_message)
        compressed_message[:compression_level] = transformed_message[:compression_level]
        
        # Inverse FFT to approximate the original message
        lossy_message = np.fft.ifft(compressed_message).real.round().astype(int)
        
        # Clamp to valid character range and convert back to a string
        compressed_body = ''.join(chr(max(0, min(255, c))) for c in lossy_message)
        
        return compressed_body, compressed_message

    @staticmethod
    def decompress_message(compressed_message, transformed_coefficients):
        """
        Decompresses the message using the stored FFT coefficients.
        
        Args:
            compressed_message (str): The compressed message string.
            transformed_coefficients (array): The retained FFT coefficients.

        Returns:
            str: The reconstructed message.
        """
        # Apply inverse FFT using the transformed coefficients
        reconstructed_message = np.fft.ifft(transformed_coefficients).real.round().astype(int)
        
        # Clamp to valid character range and convert back to a string
        decompressed_body = ''.join(chr(max(0, min(255, c))) for c in reconstructed_message)
        
        return decompressed_body


