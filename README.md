# WhatsMyName
This repository has the unified data required to perform user and username enumeration on various websites. Content is in a JSON file and can easily be used in other projects such as the ones below:

![whatsmyname](whatsmyname.png)

## Tools/Web Sites Using WhatsMyName

* https://whatsmyname.app/ - [Chris Poulter](https://twitter.com/osintcombine) created this site which draws the project's JSON file into a gorgeous and easy to use web interface.
  * Filters for category and in search results.
  * Exports to CSV and other formats.
  * Pulls the lastest version of the project's JSON file when run.
* [Recon-ng](https://github.com/lanmaster53/recon-ng) - The **Profiler Module** uses this project's JSON content.
* [Spiderfoot](https://github.com/smicallef/spiderfoot) uses this in the **sfp_account** module. There is also [this video](https://asciinema.org/a/295923) showing how to use this project using the Spiderfoot Command Line Interface (CLI).
* [sn0int](https://github.com/kpcyrd/sn0int) downloads and uses the JSON file in the [kpcyrd/whatsmyname](https://sn0int.com/r/kpcyrd/whatsmyname) module, see https://twitter.com/sn0int/status/1228046880459907073 for details and instructions.

## Content

* The https://github.com/WebBreacher/WhatsMyName/wiki/Problem-Removed-Sites page has websites that we have had in the project and are currently not working for some reason. We will retest those sites (in the future) and try to find detections.
* If you would like to help with detections, we are happy to accept them via GitHub Pull Request or you can [create an issue](https://github.com/WebBreacher/WhatsMyName/issues) with the details of the site.
* Want to suggest a site to be added? Use [this form](https://spotinfo.co/whatsmynameform).

# Format

See [CONTRIBUTING](CONTRIBUTING.md)

# Standalone Checkers
If you just want to run this script to check user names on sites and don't wish to use it in combination with another tool (like Recon-NG and/or Spiderfoot), then you can use the included Python 3 scripts as shown below. There is the `web_accounts_list_checker_threading.py` (preferred) and the `web_accounts_list_checker.py` which will take MUCH longer to cycle through all the sites. The threaded one is shown below.

```
 $  python3 ./web_accounts_list_checker_threading.py -u maxim
 -  253 sites found in file.
 >  Looking up https://www.7cups.com/@maxim
 >  Looking up https://asciinema.org/~maxim
 >  Looking up https://audiojungle.net/user/maxim
 >  Looking up https://www.biggerpockets.com/users/maxim
 >  Looking up https://www.bookcrossing.com/mybookshelf/maxim
 >  Looking up https://www.buymeacoffee.com/maxim
 >  Looking up https://www.championat.com/user/maxim/
 >  Looking up https://community.cloudflare.com/u/maxim
 >  Looking up https://www.cnet.com/profiles/maxim/
 ... SNIP ...
 >  Looking up https://www.blogger.com/profile/maxim
 >  Looking up https://armorgames.com/user/maxim

-------------------------------------------
Searching for sites with username (maxim) > Found 160 results:

[+] Found user at https://www.codewars.com/users/maxim
[+] Found user at https://about.me/maxim
[+] Found user at https://community.cloudflare.com/u/maxim
[+] Found user at https://www.designspiration.com/maxim/
[+] Found user at https://www.wowhead.com/user=maxim
[+] Found user at https://audiojungle.net/user/maxim
[+] Found user at https://f3.cool/maxim
[+] Found user at https://coderwall.com/maxim/
```
# PoC - Checker that takes screenshots of found profiles
There is a standalone Checker that will also take screenshots of found profiles and store them in a subdirectory. That script is `web_accounts_list_checker_screenshots.py`. The script is currently a rough proof-of-concept and relies on you having a working Selenium configuration, complete with the Python modules etc. You will also need to have the correct Chrome engine installed and available to the Python interpreter you run the script with.

You run the script with python3 ./web_accounts_list_checker_screenshots.py -u maxim

If the script finds at least a profile it will create a subdirectory with a name based on the current time and date plus the username you searched for. In that directory you should find a screenshot of each profile page it identified.

# Contributors
We would like to thank each of our contributors for their work. Whether it was adding sites, making our logo, fixing some broken code, or enhancing the project in many other ways! We appreciate the time you volunteered!

[@WebBreacher](https://github.com/WebBreacher/), [@Munchko](https://github.com/Munchko/), [@L0r3m1p5um](https://github.com/L0r3m1p5um/), [@lehuff](https://github.com/lehuff/), [@arnydo](https://github.com/arnydo), [@janbinx](https://github.com/janbinx/), [@bcoles](https://github.com/bcoles), [@Sector035](https://github.com/sector035/), [@mccartney](https://github.com/mccartney), [@salaheldinaz](https://github.com/salaheldinaz), [@camhoff](https://github.com/spotlightc), [@BerndDasByte](https://github.com/BerndDasByte/), [@jocephus](https://github.com/jocephus/), [@swedishmike](https://github.com/swedishmike/)

# License
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
