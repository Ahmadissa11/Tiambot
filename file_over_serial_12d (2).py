import serial
import time

real_moves = []

def process_moves(moves):
    moves = moves[::-1]
    for i in moves:
        if len(i) == 1:
            real_moves.append(i + "'")
        else:
            real_moves.append(i[0])
            
def send_file_over_serial(file_path, com_port, baud_rate=9600, timeout=1):
    """
    Reads a text file and sends its contents serially through a COM port, chunk by chunk.
    If a chunk contains a single character, it is sent as-is. If it contains multiple characters,
    only the first non-apostrophe character is sent, and it is converted to lowercase if it is an uppercase letter.

    Args:
        file_path (str): Path to the text file to be sent.
        com_port (str): COM port to which the data will be sent (e.g., "COM3").
        baud_rate (int): Baud rate for the serial communication (default: 9600).
        timeout (int): Timeout for the serial connection (default: 1 second).
    """
    try:
        # Open the serial connection
        with serial.Serial(port=com_port, baudrate=baud_rate, timeout=timeout) as ser:
            print(f"Connected to {com_port} at {baud_rate} baud.")

            # Open and read the file
            with open(file_path, 'r') as file:
                data = file.read().strip().split(" ")[:-2]  # Read and split the file content into chunks
                process_moves(data)
                data = real_moves
                print(f"Data length: {len(data)} chunks.")
                print(f"Sending file in chunks...")
                
                # Send the data chunk by chunk
                for chunk in data:
                    if len(chunk) == 1:
                        # If the chunk has one character, send it as-is
                        to_send = chunk
                    else:
                        # If the chunk has multiple characters, send the first non-apostrophe character
                        to_send = next((char for char in chunk if char != "'"), "")
                        if to_send.isupper():
                            to_send = to_send.lower()

                    if to_send:  # Ensure there is something to send
                        ser.write(to_send.encode('utf-8'))  # Send the character
                        ser.flush()  # Ensure the data is fully written to the serial buffer
                        time.sleep(1)  # Delay to ensure the receiver has time to process
                        print(f"Sent: '{to_send}' from chunk: '{chunk}'")

                print("File transmission complete.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
send_file_over_serial('solution.txt', 'COM4', baud_rate=9600)
