#!/usr/bin/python3.6
import valinorapp, sys

if __name__ == '__main__':
    #DO STUFF
    vln = valinorapp.ValinorApp(sys.argv)
    vln.run()

    sys.exit(vln.exec_())
