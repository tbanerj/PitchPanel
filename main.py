from analysis.analyzer import analyze_singing_ai

def main():
    print("Welcome to VirtuOpera: Vocal Analysis Tool")
    file = input("Enter path to .wav file (e.g., audio_samples/scale_normal.wav): ")
    notes = input("Enter reference notes (comma-separated, like C4,D4,E4): ")
    notes_list = [note.strip() for note in notes.split(',') if note.strip()]
    
    analyze_singing_ai(file, notes_list)

if __name__ == "__main__":
    main()
