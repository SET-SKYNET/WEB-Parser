# WEB-Parser
This is WEB Parser, using ChromeDriver.
So if you have a list of pages, form where you need to grab some data - this parser will grab all the data you need automatically and save you a lot of your time and nerve cells! =)

P.S. The purpose of creating this parser is not to make a profit.
The parser was created for educational purposes, for students to give a presentation on the pet project of the site for joint viewing of films. =)

To run parser example:
1. Install latest Python from here:
(https://www.python.org/downloads/)

2. Clone WEB-Parser and jump into it's directory, with next commands from the command line:
```
git clone https://github.com/SET-SKYNET/WEB-Parser.git
cd WEB-Parser
```

3. Download the latest ChromeDriver binary from here:
(https://chromedriver.chromium.org/downloads)
Then unpack and put chromedriver binary file into clonned WEB-Parser directory

4. Run Parser form the command line
```
python3 app.py --chromedriver chromedriver --deserialize_links_from parsed_links.txt --serialize_data_to films_data.xlsx
```

5. Enjoy the result, by opening films_data.xlsx
