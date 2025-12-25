import sys
import os
import locale


def to_unicode(s):
    if s is None:
        return u""
    # bytes -> decode; str (py3) or unicode (py2) -> return as-is
    if isinstance(s, bytes):
        try:
            return s.decode('utf-8')
        except Exception:
            return s.decode(sys.getfilesystemencoding(), errors='replace')
    return s

def safe_print(u):
    """
    Print `u` to the console in a way that displays correctly on Windows and Unix
    terminals. Strategy:
    - Convert input to unicode (text).
    - Try writing text directly (works on Python 3). If that raises (Py2
      or encoding mismatch), encode to the terminal/system encoding and write
      bytes. On Windows prefer 'mbcs' (the ANSI code page) so Chinese displays
      correctly in PowerShell/console.
    """
    text = to_unicode(u) + "\n"

    # Determine an encoding to use when we need to write bytes.
    enc = getattr(sys.stdout, 'encoding', None) or locale.getpreferredencoding(False)
    if os.name == 'nt':
        # On Windows, using 'mbcs' maps to the current ANSI code page (CP936 for
        # Simplified Chinese). This usually gives correct display in PowerShell
        # / cmd without requiring chcp changes.
        enc = 'mbcs'

    try:
        # Prefer writing text directly (Python 3). In Python 2 this will raise
        # UnicodeEncodeError if sys.stdout can't handle the characters.
        sys.stdout.write(text)
    except Exception:
        # Fallback: encode to the chosen encoding and write bytes.
        data = text.encode(enc or 'utf-8', errors='replace')
        try:
            # Python 3: write to buffer
            sys.stdout.buffer.write(data)
        except Exception:
            # Python 2: sys.stdout.write accepts bytes
            sys.stdout.write(data)

    try:
        sys.stdout.flush()
    except Exception:
        pass