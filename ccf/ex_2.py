#!/usr/bin/env python3

from Data import DataDescription

if __name__ == "__main__":
    a = DataDescription(
        "test",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin"
        " placerat augue vel diam elementum vestibulum rhoncus volutpat ipsum."
        " Maecenas pulvinar elit eget ullamcorper euismod. Etiam pretium vitae"
        " neque vitae mollis. Morbi dignissim tincidunt enim a ultrices. Donec"
        " iaculis sagittis est, mollis vulputate massa luctus sit amet. Proin"
        " porta lectus non purus euismod condimentum. Aenean in nisi vel odio"
        " semper dapibus nec in nisi."
    )
    print(str(a))
