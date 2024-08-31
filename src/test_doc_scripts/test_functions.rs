// Test code to implement a TCP Server in Rust
use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::thread;

fn handle_client(mut stream: TcpStream) {
    let mut buffer = [0; 512];
    loop {
        match stream.read(&mut buffer) {
            Ok(0) => break, // 
            Ok(_) => {
                stream.write(&buffer).unwrap();
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
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    println!("Server listening on port 7878");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                thread::spawn(|| handle_client(stream));
            }
            Err(e) => {
                eprintln!("Connection failed: {}", e);
            }
        }
    }
}
