
<p align="center">
  <img width="256" height="256" src="https://img.nbc66.dev/CCExporter_icon.png">
</p>

# CCExporter
This is a simple python app that can convert `closedcaption_<language>.txt` files into .json for easy import into crowdsourcing websites like
[crowdin](https://crowdin.com/)
and
[POEditor](https://poeditor.com/)

## Features

### GUI
The app has a simple built in gui which allows you to export to JSON and Back to VDF

![python_sf6rYRZSI1](https://github.com/Nbc66/CCExporter/assets/34843947/2ccc3d73-15f8-414b-be05-9a74e4d9c060)

### CLI
It also can be used in the command line by itself to allow for easy automation using GitHub Actions and GitLab's CI/CD Pipelines

![WindowsTerminal_OFhKVT62mC](https://github.com/Nbc66/CCExporter/assets/34843947/1fb513fb-c464-413b-b90b-8a14ad39ab44)

### Export back to VDF
You can Export JSON back to VDF files 

Exported VDF Files are `UTF 16 LE BOM Encoded` this is so that you can easily pass the exported VDF file into CaptionCompiler.exe to easily compile them into
Source Engine Readable `.dat` files

### Compile straight to `.dat` files

as the title says you can compile JSON files straight to `.dat` files when converting
it will spit out a `.vdf` file and a `.dat` file which you can use straight away inside the source engine

## Installing
To install this app you can simply go to the [Releases](https://github.com/Nbc66/CCExporter/releases) Section on the Repo
and download the latest `CCExporter.exe`

or you can just run the project using `python __main__.py`

## Credits

Credit to [p0358](https://github.com/p0358) for writing [source-caption-compiler](https://github.com/p0358/source-caption-compiler) and open-sourcing it so that we can now compile 
closed caption files without needing to use `CaptionCompiler.exe`
