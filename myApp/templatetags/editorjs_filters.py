"""
Template filters for rendering Editor.js content
"""
import json
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.filter(name='render_editorjs')
def render_editorjs(content):
    """
    Convert Editor.js JSON to HTML
    """
    if not content:
        return ''
    
    # Try to parse as JSON
    try:
        data = json.loads(content) if isinstance(content, str) else content
        blocks = data.get('blocks', [])
    except (json.JSONDecodeError, AttributeError, TypeError):
        # If not JSON, assume it's HTML and return as-is
        return mark_safe(content)
    
    html_parts = []
    
    for block in blocks:
        block_type = block.get('type')
        block_data = block.get('data', {})
        
        if block_type == 'paragraph':
            text = block_data.get('text', '')
            # Editor.js text may contain HTML, so we mark it safe
            html_parts.append(f'<p>{text}</p>')
        
        elif block_type == 'header':
            level = block_data.get('level', 2)
            text = block_data.get('text', '')
            html_parts.append(f'<h{level}>{text}</h{level}>')
        
        elif block_type == 'list':
            style = block_data.get('style', 'unordered')
            items = block_data.get('items', [])
            tag = 'ul' if style == 'unordered' else 'ol'
            items_html = ''.join(f'<li>{item}</li>' for item in items)
            html_parts.append(f'<{tag} class="styled">{items_html}</{tag}>')
        
        elif block_type == 'quote':
            text = block_data.get('text', '')
            caption = block_data.get('caption', '')
            html_parts.append(f'<div class="pullquote"><p>{text}</p>')
            if caption:
                html_parts.append(f'<cite>{escape(caption)}</cite>')
            html_parts.append('</div>')
        
        elif block_type == 'pullquote':
            text = block_data.get('text', '')
            citation = block_data.get('citation', '')
            html_parts.append(f'<div class="pullquote"><p>{text}</p>')
            if citation:
                html_parts.append(f'<cite>{escape(citation)}</cite>')
            html_parts.append('</div>')
        
        elif block_type == 'statCallout':
            stat1 = block_data.get('stat1', {})
            stat2 = block_data.get('stat2', {})
            stat3 = block_data.get('stat3', {})
            html_parts.append('<div class="stat-callout">')
            for stat in [stat1, stat2, stat3]:
                num = stat.get('num', '')
                label = stat.get('label', '')
                html_parts.append(f'<div class="stat-cell"><div class="num">{escape(num)}</div><div class="lbl">{escape(label)}</div></div>')
            html_parts.append('</div>')
        
        elif block_type == 'imageCaption':
            url = block_data.get('url', '')
            caption = block_data.get('caption', '')
            style = block_data.get('style', 'teal')
            if url:
                html_parts.append('<div class="article-img">')
                html_parts.append(f'<div class="article-img-inner {escape(style)}">')
                html_parts.append(f'<img src="{escape(url)}" alt="{escape(caption)}" style="width:100%;height:100%;object-fit:cover;">')
                html_parts.append('</div>')
                html_parts.append('</div>')
                if caption:
                    html_parts.append(f'<p class="img-caption">{escape(caption)}</p>')
        
        elif block_type == 'image':
            url = block_data.get('url', '')
            caption = block_data.get('caption', '')
            if url:
                html_parts.append('<div class="article-img">')
                html_parts.append('<div class="article-img-inner teal">')
                html_parts.append(f'<img src="{escape(url)}" alt="{escape(caption)}" style="width:100%;height:100%;object-fit:cover;">')
                html_parts.append('</div>')
                html_parts.append('</div>')
                if caption:
                    html_parts.append(f'<p class="img-caption">{escape(caption)}</p>')
        
        elif block_type == 'code':
            code = block_data.get('code', '')
            html_parts.append(f'<pre><code>{escape(code)}</code></pre>')
        
        elif block_type == 'delimiter':
            html_parts.append('<hr class="ce-delimiter">')
        
        elif block_type == 'linkTool':
            link = block_data.get('link', '')
            meta = block_data.get('meta', {})
            title = meta.get('title', link)
            html_parts.append(f'<p><a href="{escape(link)}">{escape(title)}</a></p>')
    
    return mark_safe(''.join(html_parts))

