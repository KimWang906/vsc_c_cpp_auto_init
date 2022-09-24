// serde_yaml, subprocess, zip, platforms, std::os, std::path::Path

use std::{path::Path, process, io, io::prelude::*};
use colored::Colorize;
use std::env;

pub trait GlobalUtilities {
    fn press_key_to_continue() {
        let mut stdin = io::stdin();
        let mut stdout = io::stdout();
    
        // We want the cursor to stay at the end of the line, so we print without a newline and flush manually.
        write!(stdout, "Press any key to continue...").unwrap();
        stdout.flush().unwrap();
    
        // Read a single byte and discard
        let _ = stdin.read(&mut [0u8]).unwrap();
    }
    
    fn check_directory_exist(directory : &str) -> bool{
        let res = Path::new(directory).is_dir();
        match res {
            true => return true,
            _ => return false
        };
    }
    
    fn clear_console() {
        print!("{}[2J", 27 as char);
    }
    
    fn end_process() {
        process::exit(0x0100);
    }
    
    fn global_warning_message_handler(message : &str) {
        println!("{}", message.truecolor(255, 204, 0));
    }
    
    fn warning_message_handler(message : &str) {
        println!("{}", message.truecolor(255, 204, 0));
    }
    
    fn error_message_handler(message : &str, additionalmsg : &str) {
        if additionalmsg == "" {
            let additionalmsg = "Additional Message Not Exist";
        }
        println!("{} : {} / {}", "Error Occured".red(), message, additionalmsg);
        Self::press_key_to_continue();
        Self::clear_console();
        Self::end_process();
    }
}

pub trait FeatureProcessorsGlobalUtilities {
    // Class : It's a class that handles each option functionally.
    // returnProjectDirectory : return list of project Directory
    // projectDirectoryChecker : if project directory not exist it genereate new directory user designate
    // help : print document
    // let __CDirectory = "C:\\";
    // let __GCCDirectory = "C:\\mingw64\\bin";
    // let __MSVCzipfile = env::current_dir().unwrap() + "\\mingw\\mingw64.zip";
    // let __batchfilesDirectory = os.getcwd() + "\\batchfiles";
    // __decompressDirectory = 'C:\\mingw64'
    // __ProjectDirectory = None
}

fn main() {
    
}