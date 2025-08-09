#!/usr/bin/env python3
"""
Script di test per verificare il funzionamento delle API AI.
Questo script testa sia Gemini che OpenAI per assicurarsi che il fallback funzioni correttamente.
"""

import os
import sys
from utils import call_gemini_api, call_openai_api

def test_api_calls():
    """Test delle chiamate API con diversi scenari."""
    
    print("🧪 TESTING API CALLS")
    print("=" * 50)
    
    # Test prompt semplice
    test_prompt = """
    Crea un breve piano alimentare per lunedì in formato JSON:
    {
        "monday": {
            "lunch": {"title": "Nome piatto", "description": "Descrizione", "focus": "Focus nutrizionale", "servings": 2},
            "dinner": {"title": "Nome piatto", "description": "Descrizione", "focus": "Focus nutrizionale", "servings": 3}
        }
    }
    """
    
    print(f"📝 Test prompt: {test_prompt[:100]}...")
    print()
    
    # Test 1: Gemini API (se disponibile)
    print("🔍 TEST 1: Gemini API")
    print("-" * 30)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print(f"✅ GEMINI_API_KEY trovata (lunghezza: {len(gemini_key)})")
        try:
            response = call_gemini_api(test_prompt)
            if "Error" in response or "Exception" in response:
                print(f"❌ Gemini ha restituito un errore: {response[:200]}...")
            else:
                print(f"✅ Gemini ha funzionato! Lunghezza risposta: {len(response)}")
                print(f"📄 Prime 200 caratteri: {response[:200]}...")
        except Exception as e:
            print(f"💥 Errore durante il test Gemini: {e}")
    else:
        print("⚠️  GEMINI_API_KEY non trovata - sarà usato il fallback")
    
    print()
    
    # Test 2: OpenAI API (se disponibile)
    print("🔍 TEST 2: OpenAI API")
    print("-" * 30)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"✅ OPENAI_API_KEY trovata (lunghezza: {len(openai_key)})")
        try:
            response = call_openai_api(test_prompt)
            if "Error" in response or "Exception" in response:
                print(f"❌ OpenAI ha restituito un errore: {response[:200]}...")
            else:
                print(f"✅ OpenAI ha funzionato! Lunghezza risposta: {len(response)}")
                print(f"📄 Prime 200 caratteri: {response[:200]}...")
        except Exception as e:
            print(f"💥 Errore durante il test OpenAI: {e}")
    else:
        print("⚠️  OPENAI_API_KEY non trovata")
    
    print()
    
    # Test 3: Scenario completo (come nell'app)
    print("🔍 TEST 3: Scenario completo (come nell'app)")
    print("-" * 30)
    
    try:
        # Questo dovrebbe seguire la logica dell'app: Gemini -> OpenAI -> Dummy
        response = call_gemini_api(test_prompt)
        
        if "weekly_plan" in response:
            print("✅ Risposta contiene 'weekly_plan' - formato corretto!")
        else:
            print("⚠️  Risposta non contiene 'weekly_plan' - potrebbe essere testo semplice")
        
        print(f"📊 Lunghezza risposta finale: {len(response)}")
        
    except Exception as e:
        print(f"💥 Errore durante il test completo: {e}")
    
    print()
    print("🏁 Test completati!")
    print("=" * 50)


def show_env_status():
    """Mostra lo stato delle variabili d'ambiente."""
    print("🔧 STATO VARIABILI D'AMBIENTE")
    print("=" * 50)
    
    env_vars = [
        "GEMINI_API_KEY",
        "OPENAI_API_KEY", 
        "MAIL_SERVER",
        "FLASK_DEBUG"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Nascondi le API keys per sicurezza
            if "API_KEY" in var:
                display_value = f"***...{value[-4:]}" if len(value) > 4 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Non impostata")
    
    print()


if __name__ == "__main__":
    print("🚀 FAME API TESTER")
    print("=" * 50)
    print()
    
    show_env_status()
    test_api_calls()
    
    print("\n💡 SUGGERIMENTI:")
    print("- Se non hai API keys, l'app userà dati di esempio")
    print("- Per Gemini: https://makersuite.google.com/app/apikey")
    print("- Per OpenAI: https://platform.openai.com/api-keys")
    print("- Imposta le variabili con: export GEMINI_API_KEY='your_key'")
