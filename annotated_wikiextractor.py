import wikiextractor


def main():
    script_name = os.path.basename(sys.argv[0])

    try:
        long_opts = ['help', 'usage', 'compress', 'bytes=', 'output=', 'keep-anchors']
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'kcb:o:', long_opts)
    except getopt.GetoptError:
        wikiextractor.show_usage(sys.stderr, script_name)
        wikiextractor.show_suggestion(sys.stderr, script_name)
        sys.exit(1)

    compress = False
    file_size = 500 * 1024
    output_dir = '.'

    for opt, arg in opts:
        if opt == '--help':
            show_help()
            sys.exit()
        elif opt == '--usage':
            wikiextractor.show_usage(sys.stdout, script_name)
            sys.exit()
        elif opt in ('-k', '--keep-anchors'):
            keep_anchors = True
        elif opt in ('-c', '--compress'):
            compress = True
        elif opt in ('-b', '--bytes'):
            try:
                if arg[-1] in 'kK':
                    file_size = int(arg[:-1]) * 1024
                elif arg[-1] in 'mM':
                    file_size = int(arg[:-1]) * 1024 * 1024
                else:
                    file_size = int(arg)
                if file_size < 200 * 1024: raise ValueError()
            except ValueError:
                wikiextractor.show_size_error(script_name, arg)
                sys.exit(2)
        elif opt in ('-o', '--output'):
            if os.path.isdir(arg):
                output_dir = arg
            else:
                wikiextractor.show_file_error(script_name, arg)
                sys.exit(3)

    if len(args) > 0:
        wikiextractor.show_usage(sys.stderr, script_name)
        wikiextractor.show_suggestion(sys.stderr, script_name)
        sys.exit(4)

    wiki_extractor = AnnotatedWikiExtractor()
    output_splitter = wikiextractor.OutputSplitter(compress, file_size, output_dir)
    process_data(sys.stdin, wiki_extractor, output_splitter)

    output_splitter.close()


if __name__ == '__main__':
    main()