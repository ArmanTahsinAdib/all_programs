use crossterm::{
    cursor,
    event::{self, Event, KeyCode},
    execute,
    style::{Color, Print, ResetColor, SetForegroundColor},
    terminal::{self, disable_raw_mode, enable_raw_mode, Clear, ClearType},
    ExecutableCommand,
};
use std::io::{self, Write};
use std::time::{Duration, Instant};
use rand::seq::SliceRandom;
use rand::thread_rng;

const WORDS: &[&str] = &[
    "apple", "banana", "orange", "grape", "pineapple", "strawberry", "blueberry", "kiwi", "peach", "mango",
    "watermelon", "cherry", "lemon", "lime", "plum", "pear", "apricot", "blackberry", "coconut", "papaya",
];

fn generate_test_text(word_count: usize) -> String {
    let mut rng = thread_rng();
    WORDS.choose_multiple(&mut rng, word_count).cloned().collect::<Vec<_>>().join(" ")
}

fn calculate_wpm(start_time: Instant, word_count: usize) -> f64 {
    let elapsed_secs = start_time.elapsed().as_secs_f64();
    (word_count as f64 / elapsed_secs) * 60.0
}

fn main() -> crossterm::Result<()> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();

    let word_count = 30;
    let text_to_type = generate_test_text(word_count);
    let mut user_input = String::new();
    let mut start_time: Option<Instant> = None;
    let mut finished = false;

    let (cols, rows) = terminal::size()?;

    loop {
        // Clear the screen
        stdout.execute(Clear(ClearType::All))?;

        // Calculate the centered position
        let text_len = text_to_type.len() as u16;
        let start_x = (cols / 2).saturating_sub(text_len / 2);
        let start_y = rows / 2;

        // Move the cursor to the calculated position
        stdout.execute(cursor::MoveTo(start_x, start_y))?;

        // Display the text to type with contrast
        for (i, expected_char) in text_to_type.chars().enumerate() {
            if i < user_input.len() {
                let typed_char = user_input.chars().nth(i).unwrap();
                if typed_char == expected_char {
                    // Correct character: display in bright white
                    stdout.execute(SetForegroundColor(Color::White))?;
                    print!("{}", typed_char);
                } else {
                    // Incorrect character: display in red
                    stdout.execute(SetForegroundColor(Color::Red))?;
                    print!("{}", typed_char);
                }
            } else {
                // Untyped text: display in dark gray
                stdout.execute(SetForegroundColor(Color::DarkGrey))?;
                print!("{}", expected_char);
            }
        }

        // Place the cursor after the last typed character
        let cursor_position = user_input.len().min(text_to_type.len()) as u16;
        stdout.execute(cursor::MoveTo(start_x + cursor_position, start_y))?;
        
        // Display the line-shaped cursor
        stdout.execute(SetForegroundColor(Color::White))?;
        print!("|"); // Use a line character for the cursor
        stdout.execute(ResetColor)?;

        // End typing test when the input matches the text
        if user_input == text_to_type {
            finished = true;
        }

        if finished {
            let elapsed_time = start_time.unwrap().elapsed();
            let wpm = calculate_wpm(start_time.unwrap(), word_count);
            stdout.execute(cursor::MoveTo(start_x, start_y + 2))?;
            println!(
                "\nTest complete! WPM: {:.2}, Time: {:.2} seconds",
                wpm,
                elapsed_time.as_secs_f64()
            );
            break;
        }

        // Capture user input
        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key_event) = event::read()? {
                match key_event.code {
                    KeyCode::Char(c) => {
                        if start_time.is_none() {
                            start_time = Some(Instant::now());
                        }
                        user_input.push(c);
                    }
                    KeyCode::Backspace => {
                        user_input.pop();
                    }
                    KeyCode::Esc => break, // Exit on ESC
                    _ => {}
                }
            }
        }

        stdout.flush()?;
    }

    // Hide the default cursor
    stdout.execute(cursor::Hide)?;
    disable_raw_mode()?;
    Ok(())
}
