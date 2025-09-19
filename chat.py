#!/usr/bin/env python3

"""
Interactive chat client for Rasa RAG Chatbot
A simple Python script to chat with the bot in terminal
"""

import requests
import json
import sys

class RasaChatClient:
    def __init__(self, rasa_url="http://localhost:5005", sender_id="user"):
        self.rasa_url = rasa_url
        self.sender_id = sender_id
        self.webhook_url = f"{rasa_url}/webhooks/rest/webhook"
        
    def send_message(self, message):
        """Send message to Rasa and get response"""
        try:
            payload = {
                "sender": self.sender_id,
                "message": message
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return [{"text": f"Error: Server returned {response.status_code}"}]
                
        except requests.exceptions.ConnectionError:
            return [{"text": "Error: Could not connect to Rasa server. Is it running?"}]
        except Exception as e:
            return [{"text": f"Error: {str(e)}"}]
    
    def chat(self):
        """Start interactive chat session"""
        print("🤖 Rasa RAG Chatbot")
        print("=" * 50)
        print("Type your messages below. Use 'quit', 'exit', or Ctrl+C to end.")
        print("Upload PDFs first, then ask questions about their content!")
        print("=" * 50)
        
        try:
            while True:
                # Get user input
                user_message = input("\n💬 You: ").strip()
                
                # Check for exit commands
                if user_message.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("👋 Bot: Goodbye!")
                    break
                
                if not user_message:
                    continue
                
                # Send message to bot
                responses = self.send_message(user_message)
                
                # Display bot responses
                for response in responses:
                    if 'text' in response:
                        print(f"🤖 Bot: {response['text']}")
                    elif 'image' in response:
                        print(f"🤖 Bot: [Image: {response['image']}]")
                    elif 'custom' in response:
                        print(f"🤖 Bot: {json.dumps(response['custom'], indent=2)}")
                        
        except KeyboardInterrupt:
            print("\n👋 Chat ended. Goodbye!")
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    # Parse command line arguments
    rasa_url = "http://localhost:5005"
    sender_id = "user"
    
    if len(sys.argv) > 1:
        rasa_url = sys.argv[1]
    if len(sys.argv) > 2:
        sender_id = sys.argv[2]
    
    # Create chat client and start chatting
    client = RasaChatClient(rasa_url, sender_id)
    client.chat()

if __name__ == "__main__":
    main()