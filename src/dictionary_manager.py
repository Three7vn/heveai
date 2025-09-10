#!/usr/bin/env python3
"""
Dictionary Manager CLI tool for managing vocabulary corrections
"""
import argparse
import json
from pathlib import Path
from dictionary_corrector import DictionaryCorrector

def main():
    parser = argparse.ArgumentParser(description="Manage vocabulary dictionary for Heve AI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add replacement command
    add_parser = subparsers.add_parser('add', help='Add word replacement')
    add_parser.add_argument('wrong', help='Incorrectly transcribed word')
    add_parser.add_argument('correct', help='Correct word')
    
    # Add technical term command
    term_parser = subparsers.add_parser('term', help='Add technical term')
    term_parser.add_argument('term', help='Technical term to add')
    
    # List dictionary contents
    list_parser = subparsers.add_parser('list', help='List dictionary contents')
    
    # Test correction
    test_parser = subparsers.add_parser('test', help='Test correction on text')
    test_parser.add_argument('text', help='Text to test correction on')
    
    # Stats
    stats_parser = subparsers.add_parser('stats', help='Show dictionary statistics')
    
    args = parser.parse_args()
    
    corrector = DictionaryCorrector()
    
    if args.command == 'add':
        corrector.add_replacement(args.wrong, args.correct)
        print(f"Added replacement: '{args.wrong}' → '{args.correct}'")
    
    elif args.command == 'term':
        corrector.add_technical_term(args.term)
        print(f"Added technical term: '{args.term}'")
    
    elif args.command == 'list':
        print("=== REPLACEMENTS ===")
        for wrong, correct in corrector.dictionary["replacements"].items():
            print(f"  {wrong} → {correct}")
        
        print("\n=== TECHNICAL TERMS ===")
        for term in corrector.dictionary["technical_terms"]:
            print(f"  {term}")
    
    elif args.command == 'test':
        original = args.text
        corrected = corrector.apply_real_time_corrections(original)
        print(f"Original:  {original}")
        print(f"Corrected: {corrected}")
    
    elif args.command == 'stats':
        stats = corrector.get_correction_stats()
        print("=== DICTIONARY STATISTICS ===")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
