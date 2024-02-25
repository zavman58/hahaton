from partners import main
import sys

if sys.argv[1] == '0':
	id = None
	d = ' '.join(sys.argv[2:])
elif sys.argv[1] == '1':
	id = sys.argv[3].split('/')[-1]
	d = ' '.join(sys.argv[4:])
else:
	id = sys.argv[3].split('/')[-2]
	d = ' '.join(sys.argv[4:])

sys.stdout.write(str(main(sys.argv[1], d, id)))
sys.stdout.flush()
sys.exit(0)

