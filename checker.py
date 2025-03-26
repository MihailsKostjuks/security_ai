import re
import random
import string
import math
import hashlib

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345",
    "111111", "1234567", "sunshine", "qwerty", "iloveyou", "admin"
}

BREACHED_PASSWORDS = {
    "letmein", "123456", "password1", "welcome123", "qwertyuiop"
}

password_history = []

def calculate_entropy(password):
    pool = 0
    if re.search(r'[a-z]', password): pool += 26
    if re.search(r'[A-Z]', password): pool += 26
    if re.search(r'\d', password): pool += 10
    if re.search(r'[@$!%*?&]', password): pool += len("@$!%*?&")
    if pool == 0: return 0
    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def check_password_strength(password):
    score = 0
    feedback = []

    if password in COMMON_PASSWORDS:
        feedback.append("Password is too common.")
        return score, feedback

    if password in BREACHED_PASSWORDS:
        feedback.append("This password has been found in data breaches.")
        return score, feedback

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r'[a-z]', password): score += 1
    else: feedback.append("Add lowercase letters.")

    if re.search(r'[A-Z]', password): score += 1
    else: feedback.append("Add uppercase letters.")

    if re.search(r'\d', password): score += 1
    else: feedback.append("Add digits.")

    if re.search(r'[@$!%*?&]', password): score += 1
    else: feedback.append("Add special characters (@$!%*?&).")

    return score, feedback

def strength_label(score):
    if score <= 2: return "Weak"
    elif score == 3: return "Moderate"
    else: return "Strong"

def generate_password(length=12, use_digits=True, use_symbols=True):
    chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += "@$!%*?&"
    return ''.join(random.choice(chars) for _ in range(length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def print_history():
    if not password_history:
        print("No password checks yet.")
        return
    for i, item in enumerate(password_history, 1):
        print(f"{i}. Strength: {item['strength']}, Entropy: {item['entropy']} bits")
        print(f"   Password Hash: {item['hash'][:20]}...")

def main():
    print("=== Mini Cybersecurity Password Tool ===")
    while True:
        print("\nMenu:")
        print("1: Check Password Strength")
        print("2: Generate Secure Password")
        print("3: View Password History")
        print("4: Exit")
        choice = input("Choose: ")

        if choice == "1":
            pwd = input("Enter your password: ")
            score, tips = check_password_strength(pwd)
            entropy = calculate_entropy(pwd)
            hash_val = hash_password(pwd)
            result = {
                'password': pwd,
                'strength': strength_label(score),
                'entropy': entropy,
                'hash': hash_val
            }
            password_history.append(result)

            print(f"\nStrength: {result['strength']}")
            print(f"Entropy: {result['entropy']} bits")
            print(f"SHA-256 Hash: {hash_val[:40]}...")
            if tips:
                print("Suggestions:")
                for tip in tips:
                    print(f"- {tip}")
            else:
                print("Your password is strong!")

        elif choice == "2":
            try:
                length = int(input("Password length (default 12): ") or 12)
                use_digits = input("Include digits? (y/n): ").lower() == 'y'
                use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
                new_pwd = generate_password(length, use_digits, use_symbols)
                print(f"Generated password: {new_pwd}")
            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            print("\n--- Password Check History ---")
            print_history()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
