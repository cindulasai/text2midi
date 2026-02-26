# -*- coding: utf-8 -*-
"""Remove emoji from node files for Windows console compatibility."""
from pathlib import Path

emoji_map = {
    '🧠': '[BRAIN]',
    '🎵': '[MUSIC]',
    '✅': '[OK]',
    '❌': '[ERROR]',
    '⚠️': '[WARN]',
    '💾': '[SAVE]',
    '📝': '[INFO]',
    '🔧': '[FIX]',
    '📊': '[STATS]',
    '🎼': '[THEORY]',
    '🎹': '[PIANO]',
    '→': '[ARROW]',
    '🔄': '[LOOP]',
    '🎯': '[TARGET]',
    '📨': '[MESSAGE]',
    '👋': '[WAVE]',
}

# Fix node files
for node_file in Path('src/agents').glob('*_node.py'):
    content = node_file.read_text(encoding='utf-8')
    for emoji, replacement in emoji_map.items():
        content = content.replace(emoji, replacement)
    node_file.write_text(content, encoding='utf-8')
    print(f"Fixed: {node_file}")

# Fix main.py
main_file = Path('main.py')
if main_file.exists():
    content = main_file.read_text(encoding='utf-8')
    for emoji, replacement in emoji_map.items():
        content = content.replace(emoji, replacement)
    main_file.write_text(content, encoding='utf-8')
    print(f"Fixed: {main_file}")

print("All emoji removed from files")

