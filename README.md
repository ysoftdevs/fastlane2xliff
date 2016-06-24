# fastlane to XLIFF converter

Simple Python tool which can convert fastlane version of resources stored in files into XLIFF.
This version of tool was tested with Python 2.7 and Trados.

You can find more information about fastlane at: https://fastlane.tools/

## Usage

`python bin/fastlane2xliff.py <soure-directory> <target-xliff-file> <language-code>`

Sample:

`python bin/fastlane2xliff.py sample/src sample/result/cs-CZ/tram.xlf "cs-CZ"`

`python bin/fastlane2xliff.py sample/src sample/result/sk-SK/tram.xlf "sk-SK"`

## Further information

You can find more information about development in Y Soft RnD at http://www.ysofters.com

## Author

Juraj Michalek - https://github.com/georgik
