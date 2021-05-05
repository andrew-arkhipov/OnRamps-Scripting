# Canvas Scripting Tutorial

The following is a tutorial on how to use Selenium to automate tasks in Canvas. Keep in mind that Canvas' source code is constantly changing, so the scripts will likely break over time. The intention here is to explain how to read the source code when it changes so that the appropriate changes can be made to scripts. 

Furthermore, this tutorial assumes you have some sort of understanding of Python. If you don't, don't worry, there are plenty of online resources to learn it, such as [this](https://www.codecademy.com/catalog/language/python) one. At any rate, using Selenium is really straightforward, so just a novice understanding of Python is enough. If you're stuck, [Stack Overflow](https://stackoverflow.com/) has almost every answer for any question you could possibly run into (many consider being able to search Stack Overflow and Google a skill itself, so don't feel bad if you feel overwhelmed by the sheer amount of digging you might have to do - it's part of what being a software engineer is all about).

You should also know how to use the command line interface on your computer (Terminal on Mac and WSL on Windows).

<br>

## Getting Started

Download the latest version of Python from [here](https://www.python.org/downloads/) if you don't already have it. When writing and executing scripts, you should always use a virtual environment in order to avoid cluttering up your computer. To do so, run the following commands:

```
python3 -m venv <virtual-env-name>

source <virtual-env-name>/bin/activate

pip install -r requirements.txt
```

<b>Note:</b> Make sure the `requirements.txt` file is in the same directory as your script (e.g. in `/path/to/script`) before executing the commands. The final command installs all the dependencies needed to run your scripts, so you shouldn't worry about installing new packages or libraries for scripts unless you're doing more advanced work. 

You can name your virtual environment whatever you please (the convention is `venv`). When you're done working on or running a script, simply run the following to exit the virtual environment:

```
deactivate
```

To reactivate the virtual environment, which is necessary for running a script since that's where all the script's dependencies are installed, run the following:

```
source <virtual-env-name>/bin/activate
```

<br>
<br>

## Using Selenium

A note about scripts: Selenium is *not* something that can be run automatically and in a headless state (e.g. without having a browser window open). The primary usage of Selenium is testing websites, so many of the scripts you end up writing will involve manual guessing and checking of what works and what doesn't, rather than having a robust API that can directly manipulate whatever you want. I have personally run into many instances where a script just wasn't possible, so keep that in mind as you write your first scripts.

<br>
<br>

### XPath

For most of the interactions you need to make in your scripts, you'll need to use strings which are known as XPath strings. In order to build these strings, a very basic understanding of HTML is needed. Let's go through an example.

Here is a basic set of HTML:

```
<html>
    <body>
        <div id="header" class="this-class-does-nothing">
            <h3>Hello, world!</h3>
            <button type="button>Click me!</button>
        </div>
        <div id="main-content">
            <p>This is the main content.</p>
            <button type="button">No, click me!</button>
        </div>
        <div id="tricky-content">
            <div>
                <h4>Tricky section one</h4>
            </div>
            <div>
                <h4>Tricky section two</h4>
            </div>
        </div>
    </body>
</html>
```

If you need some resources for understanding how to interpret HTML, [this](https://www.w3schools.com/html/default.asp) link should help you out.

The way XPath strings work is the exact same way navigating a file structure in the command line works, except there is no need for knowing the absolute path of a desired item (since Selenium will do the heavy lifting for you). For example, if I want to locate a button in this code, the XPath string for that is: 

```
//button
```

You may have noticed that there are multiple buttons, so the XPath above is just going to find the first one in the HTML code and return that. There's a simple fix for that. Let's say you want to locate the button that says <b>"No, click me!"</b>. There are multiple possible XPath strings for that, so let's take a look at some of them.

<br>

<b>Example 1</b>

```
//button[text()='No, click me!']
```

This is the most straightforward approach of finding an element that has some sort of text between its HTML tags. Generally speaking, adding brackets next to the item with some sort of identifier function will allow you to increase the granularity of what you're searching for. We'll explore this in further detail soon. Note that this will *not* work for text that's within child elements of a given element. For example, the above XPath string won't find the button in the following code, even though functionally speaking, they do the exact same thing.

```
<button type="button">
    <span>Click Me!</span>
</button>
```

<br>

<b>Example 2</b>
```
//button[contains(text(), 'No')]
```

This one is basically exactly the same as the above, it just allows for more leniency. The `contains` function takes two arguments: the attribute you're looking for, which in this case is `text()`, and the actual attribute value itself. The `contains` function can be used for more than `text()`, but `text()` is used for the overwhelming majority of cases.

<br>

<b>Example 3</b>

```
//div[@id='main-content']/button
```

This example is representative of the XPath strings you'll likely be writing the most. Selenium can't always find what you're looking for, so adding parent/child components makes it easier to search. In the example above, Selenium knows to look for a `div` element with `id` equal to `main-content`. For any native attributes of HTML elements, make sure to put an `@` before the attribute name itself in order to tell Selenium what to look for (e.g. `id`, `class`, `style`, etc.).

<br>

To make things a little more concrete, XPath strings function exactly the same as navigating a file structure in the command line, as mentioned earlier. For example, if you want to access the first `div` element that houses the <b>"Tricky section one"</b> text, the following XPath string will work:

```
//div[@id='tricky-content']/div/h4[text()='Tricky section one']/..
```

Notice the `..` at the end of the path. Just like in the command line (e.g. running `cd ..`), this will take you up one level in the HTML structure, and you can proceed with manipulating that new level. This is useful when parent elements don't have unique identifiers, but child elements of that parent do.

A final note: the `//` at the beginning of the path indicates to Selenium that the rest of the structure in the XPath could be locating anywhere in the HTML. If you use a single `/`, you must start from the root of the HTML body. I wouldn't recommend this, as using the the relative `//` has always been enough for any usage in Canvas.

This was a very brief overview of how XPath strings work. We will see more examples later on, but if you need more help, [here](https://www.w3schools.com/xml/xpath_intro.asp) is a resource for exploring them further.

We'll now move onto actual code.

<br>
<br>

### Driver

Selenium operates using a driver for a given web browser. There are two ways to create said driver in a given script: manually pointing the code to a driver executable in your computer, or using the `webdriver_manager` library in Python. The latter option is far easier to work with, so we will be using that. Furthermore, this tutorial assumes usage of Chrome as the browser. This can be adapted later for Firefox, if desired.

To create a driver, write the following lines (and imports) in your script.

```
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

You will be using this `driver` object for essentially every command in your script. [Here](https://selenium-python.readthedocs.io/api.html) is the documentation for the `webdriver` API in case you have further questions or need information for advanced usage.

The most basic usage of the driver is getting to a website. To do this, use the following method:

```
driver.get("https://this-can-be-any-url.com")
```

or

```
url = "https://onramps.instructure.com"
driver.get(url)
```

<br>
<br>

### Using XPath with Driver

Interacting with elements on a page is straightforward once you know how to use XPath strings. The driver object we created earlier comes with a plethora of methods for this, and the most common one is `find_element_by_xpath`. Let's see a basic example using the HTML code from above.

```
driver.find_element_by_xpath("//div[@id='main-content']/button")
```

Notice that we're using double quotes around the entire XPath string, but single quotes around the `id` attribute of the div. Make sure to use this same quoting convention when writing scripts in order to avoid getting errors from Python.

Now that we found the button, Selenium makes it really simple to interact with it. The following two pieces of code accomplish the same thing.

```
driver.find_element_by_xpath("//div[@id='main-content']/button).click()
```

```
button = driver.find_element_by_xpath("//div[@id='main-content']/button)
button.click()
```

These examples show us two things: Selenium's find methods return an object on the web page that can be interacted with the code, and multiple interactions can be chained together to perform an action.

<br>

<b>Quick tip:</b> the HTML attributes of these web page objects (referred to by Selenium as `WebElement` objects) are accessible with the `get_attribute` method. For example, if the button type is desired, the following line will get that:

```
button_type = button.get_attribute('type')
```

Text between the HTML tags can also be accessed with the following (noticed that it is a Python attribute, and not a method like the above):

```
button_text = button.text
```
You can also use the `find_element_by_xpath` method on `WebElement` objects (e.g. the button) themselves. This makes it really convenient to interact with child elements of an object without having to make Selenium search everything all over again. 

<br>

As provided earlier, [this](https://selenium-python.readthedocs.io/api.html) link provides all the methods you will ever need for finding elements with the driver. I've legitimately only used the `get`, `find_element_by_xpath`, and `switch_to.default_content` methods in my scripts, the final of which is useful for interacting with SpeedGrader.

<br>
<br>

### WebDriverWait

This topic is a bit more advanced, but it will save you a ton of time when it comes to actually running your scripts, so it's important to learn. The purpose of `WebDriverWait` is exactly like it sounds: explicitly telling the driver to wait for a certain action to occur before proceeding with the script. This is important because it allows web elements to load first before interacting with them, which we all know is vital when dealing with slow software like Canvas. 

Theoretically speaking, you could just use the `sleep` function from Python's built in `time` library in order to wait for elements to load, but this is inefficient from a runtime perspective, and is error prone.

To use `WebDriverWait', include the following lines at the top of your script file in order to import all the necessary dependencies:

```
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
```

`WebDriverWait` is the main workhorse here, and `expected_conditions` (a.k.a `EC`) and `By` are used as helper objects by `WebDriverWait` in order for it to know what to wait for and what to do with it once it's present. Let's run through an example I've personally used.

```
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='students_selectmenu-button']")))
except:
    print("Sorry, student menu button not found!")
```

This piece of code uses Python's `try`/`except` syntax, which should always be used to handle exceptions thrown in the case that `WebDriverWait` does not find what it's looking for. If you do not put the `WebDriverWait` code inside a `try`/`except` block and it's unable to find the element you're looking for, the script will crash and have to be rerun. `WebDriverWait` accepts two arguments: the `driver` object itself that we worked with before, and an amount of time to wait before throwing an exception (in this case it's 10 seconds). This is followed by the `until` method, which accepts a  single (but complex) argument. Let's break it down.

`EC` is an object that has a ton of different methods which do exactly what they sound like. In this case, `WebDriverWait` is being told by `EC` to wait for the element that is being searched for to be clickable. How are we searching for the element? By XPath! 

Notice that the argument provided to the `element_to_be_clickable` method is a single Python tuple (hence the second set of parentheses), where the first element of the tuple is `By.XPATH`, and the second is the actual XPath string. This will be the form of what you provide as an argument to the `EC` methods 99% of the time, so simply copying and pasting this line and simply changing the XPath and perhaps the `EC` method will be more than enough. The only other `EC` methods I've used are `presence_of_element_located` and `frame_to_be_available_and_switch_to_it`, the latter of which is useful for SpeedGrader.

Just like the `driver`, `WebDriverWait` returns the `WebElement` object that it found. So just like the button, the object can be stored in a variable, or other `WebElement` methods such as `click` can be chained onto it to perform multiple actions. 

<br>
<br>

## Conclusion

Believe it or not, this really covers most of what you'll need to write effective scripts. The rest of it comes from knowing how to use Python correctly, which is outside of the scope of what I'm teaching here, though it's very easy to pick up in a matter of days. At the time of writing this, I'm in my final weeks of my time at OnRamps and getting ready to move to Chicago, but I'm always happy to answer any questions you may have regarding writing scripts. Please reach out to Mark Townsend,  Emily Jensen, or Jeremiah Lucas for my email address if needed.

I've provided many examples of functions you can simply copy and paste into your scripts so that you don't have to reinvent the wheel. The way I've written the functions is similar to how `WebDriverWait` works: your `driver` object will be the first argument, and then the rest will be based on the requirements of what you're trying to accomplish. The descriptions of the arguments required are provided in the docstrings of each function with the following format:

```
def function(arg1, arg2, ...):
    """
    function description

    :param argument_type arg1: arg1 description
    :param argument_type arg2: arg2 description
    ...

    :return return_type return_item: return_item description
    """

    ...
    return return_item
```

This should be enough to explain what each function is doing, but if not, Google is your friend. :)