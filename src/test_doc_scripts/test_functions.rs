// Test code to implement a TCP Server in Rust
use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::thread;

// Function to handle client connections
fn handle_client(mut stream: TcpStream) {
    let mut buffer = [0; 512]; // Buffer to store incoming data
    loop {
        match stream.read(&mut buffer) {
            Ok(0) => break, // Connection closed by client
            Ok(_) => {
                // Echo the received data back to the client
                if let Err(e) = stream.write(&buffer) {
                    eprintln!("Error writing to socket: {}", e);
                    break;
                }
                println!(
                    "Received and sent back: {}",
                    String::from_utf8_lossy(&buffer)
                );
            }
            Err(e) => {
                eprintln!("Error reading from socket: {}", e);
                break;
            }
        }
    }
}

fn main() {
    // Bind the TCP listener to the specified address and port
    let listener = TcpListener::bind("127.0.0.1:7878").expect("Failed to bind to address");
    println!("Server listening on port 7878");

    // Accept incoming connections in a loop
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                // Spawn a new thread to handle the client connection
                thread::spawn(|| {
                    handle_client(stream);
                });
            }
            Err(e) => {
                eprintln!("Error accepting connection: {}", e);
            }
        }
    }
}
