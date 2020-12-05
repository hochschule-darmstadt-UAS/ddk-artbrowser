#import entities

from etl.xml_importer.parseLido import _parse_lido_file

if __name__ == '__main__':
    lidoFile = 'merged.xml'
    _parse_lido_file(lidoFile)