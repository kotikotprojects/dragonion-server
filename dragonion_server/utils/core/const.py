import sys


portable = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
