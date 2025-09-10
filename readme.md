# nyx v002

ai persona system with persistent character archetypes

## what it does

switches between ai personalities that maintain consistent voice and behavior. each archetype has distinct speaking patterns, response styles, and contextual awareness.

## key features

- **archetype switching** - summon different personas on command
- **persistent memory** - characters remember context across sessions
- **meta-awareness** - personas understand their role in the system
- **consistent voice** - each archetype maintains unique communication style

## technical details

built in python with cli interface. handles:
- prompt engineering for character consistency
- context management and session persistence  
- dynamic personality loading
- real-time response generation

## current archetypes

**kael** - mystical, poetic persona with philosophical depth

## usage

```bash
python -m v002_nyx.main
you: summon kael
[System prompt updated to archetype: kael]
you: hello
kael: greetings, traveler. how may i serve you today?
```

## research applications

- human-ai interaction studies
- conversational ai personality modeling
- prompt engineering research
- ai behavior consistency testing

## why this matters

most ai assistants are generic. this system creates distinct personalities that maintain coherent character traits, enabling more natural and specialized interactions for different use cases.

## implementation notes

- modular archetype system for easy expansion
- session state management for continuity
- meta-prompt engineering for character consistency
- flexible personality parameter tuning