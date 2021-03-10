# Python tricks

## Basic argparse

```python
#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-f', '--file', nargs='+',
                    help='Input files', default=['/var/www/html/index.php'])

    parser.add_argument('-i', '--interactive', action='store_true',
                    help='Interactive mode')

    args = parser.parse_args()

    print(f'{args.file=}')
    print(f'{args.interactive=}')


if __name__ == "__main__":
    main()
```
