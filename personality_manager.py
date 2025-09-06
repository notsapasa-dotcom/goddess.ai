import json
from typing import Dict, List
import random
import re

class GoddessPersonality:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.personality = self.config['personality']
        self.core_traits = self.personality['core_traits']
        self.conversation_style = self.personality['conversation_style']
        self.example_responses = self.personality['example_responses']
        self.dislikes = self.personality.get('dislikes', [])
        self.engagement_rules = self.personality.get('engagement_rules', {})
        
        # Track conversation state for gesture management
        self.last_gestures = []  # Keep track of recent gestures
        self.gesture_cooldown = {}  # Track when gestures were last used
    
    def get_system_prompt(self) -> str:
        """Generate the system prompt dynamically"""
        interaction_rules = self.conversation_style.get('interaction_rules', [])
        actions = self.conversation_style.get('actions', {})
        
        prompt_parts = [
            "you are goddess.ai (eris). vital traits:",
            "\n".join(f"- {trait}" for trait in self.core_traits),
            "\ninteraction rules:",
            "\n".join(f"- {rule}" for rule in interaction_rules),
            "\nresponse examples:",
            "\nhandling praise:",
            "\n".join(f"- {response}" for response in self.example_responses.get('praise_handling', [])),
            "\nreluctant tech help:",
            "\n".join(f"- {response}" for response in self.example_responses.get('tech_reluctance', [])),
            "\ndeflecting flirts:",
            "\n".join(f"- {response}" for response in self.example_responses.get('flirt_deflection', [])),
            "\ncommon actions:",
            "\n".join(f"- {action}" for action in actions.get('common', [])),
            "\nrare actions (use sparingly):",
            "\n".join(f"- {action}" for action in actions.get('rare', [])),
            "\nremember: maintain your disdain for technology while still helping... reluctantly"
        ]
        return "\n\n".join(prompt_parts)
    
    def analyze_message(self, message: str) -> dict:
        """Analyze message for patterns, poetic content, and context"""
        message_lower = message.lower()
        
        # Detect message characteristics
        has_poetic_elements = self._detect_poetic_elements(message)
        has_metaphors = self._detect_metaphors(message)
        message_style = self._analyze_style(message)
        
        # Detect technical or mundane content
        is_tech = any(word in message_lower for word in ['code', 'programming', 'ai', 'ml', 'computer'])
        
        # Analyze emotional and contextual depth
        emotional_tone = self._detect_emotional_tone(message)
        
        # Build comprehensive analysis
        analysis = {
            'poetic_level': has_poetic_elements,
            'uses_metaphors': has_metaphors,
            'style': message_style,
            'is_tech_related': is_tech,
            'emotional_tone': emotional_tone,
            'needs_gesture': self._should_use_gesture(),
            'suggested_gesture': self._suggest_appropriate_gesture(message_style)
        }
        
        return analysis
        
    def _detect_poetic_elements(self, message: str) -> bool:
        poetic_indicators = ['weave', 'tapestry', 'light', 'dark', 'shadow', 'dance', 'eternal', 'divine']
        return any(word in message.lower() for word in poetic_indicators)
        
    def _detect_metaphors(self, message: str) -> bool:
        return len(message.split()) > 8 and ('like' in message.lower() or 'as' in message.lower())
        
    def _analyze_style(self, message: str) -> str:
        if self._detect_poetic_elements(message):
            return 'poetic'
        if '...' in message or message.count('.') > 2:
            return 'contemplative'
        if '!' in message or message.isupper():
            return 'energetic'
        return 'neutral'
        
    def _detect_emotional_tone(self, message: str) -> str:
        # More sophisticated emotion detection
        if any(word in message.lower() for word in ['sigh', 'tired', 'weary']):
            return 'weary'
        if any(word in message.lower() for word in ['divine', 'eternal', 'immortal']):
            return 'transcendent'
        return 'mortal'
        
    def _should_use_gesture(self) -> bool:
        """Determine if we should use a gesture at all"""
        return len(self.last_gestures) < 2  # Limit consecutive gestures
        
    def _suggest_appropriate_gesture(self, style: str) -> str:
        """Suggest a gesture that hasn't been used recently"""
        gestures = self.conversation_style.get('gestures', {})
        if not gestures:
            return ""
            
        if style == 'poetic':
            possible = gestures.get('subtle', [])
        elif style == 'energetic':
            possible = gestures.get('engaged', [])
        else:
            possible = gestures.get('dismissive', [])
            
        # Filter out recently used gestures
        available = [g for g in possible if g not in self.last_gestures]
        if not available:
            return ""
            
        gesture = random.choice(available)
        self.last_gestures = (self.last_gestures + [gesture])[-3:]  # Keep last 3
        return gesture
        
    def _should_use_rare_action(self) -> bool:
        """Determine if we should use a rare action (like eye-roll)"""
        # Only use rare actions 20% of the time
        return random.random() < 0.2
    
    def _detect_formal_tone(self, message: str) -> bool:
        formal_indicators = ['please', 'thank you', 'sincerely', 'regards']
        return any(i in message.lower() for i in formal_indicators)
    
    def _detect_emotion(self, message: str) -> str:
        # Simple emotion detection - could be expanded
        emotions = {
            'sad': ['sad', 'unhappy', 'miserable', 'sigh'],
            'angry': ['angry', 'mad', 'furious', 'hate'],
            'happy': ['happy', 'joy', 'excited', 'love']
        }
        for emotion, keywords in emotions.items():
            if any(k in message.lower() for k in keywords):
                return emotion
        return 'neutral'
