OnetimeDNS.net - A free name for your dynamic IP device
==============

What
----
    Free, short and permanent... actually no, not really.
    Free, long and somewhat permanent name for your dynamic IP device.
    The name is yours while you are making HTTP requests to our API.

Again, what?
------------
          \           /
           \         /                                                                        _______
            \       /                                                                        |       |
          /~~~~~~~~~~/|  ---> curl "https://onetimedns.net/set?name=bob&secret=Ksdfh9" --->  |  one  |
         /   ----   / /                                                                      |  time |
        /_________ / /        <----- { name: bob.3x3...98x.onetimedns.net } <-----           |  DNS  |
        | o o o o | /                                                                        | .net  |
        v~~~~~~~~~v      ---> (wait 5 minutes; curl ... again; repeat forever)               |_______|


        > ping bob.3xt...98w.onetimedns.net
        PING bob.3xt...98w.onetimedns.net (228.89.121.90): 56 data bytes
        64 bytes from 228.89.121.90: icmp_seq=0 ttl=50 time=13.968 ms
        64 bytes from 228.89.121.90: icmp_seq=1 ttl=49 time=12.071 ms
        64 bytes from 228.89.121.90: icmp_seq=2 ttl=50 time=14.171 ms

Why would you need it
--------
    Well, for instance, you could access your router or Raspberry Pi or any other device that
    uses a static name, for that matter. And you could even setup a mail server at home.

How
---
        > curl "https://onetimedns.net/set?name=myname&secret=random_string"

        {
          "expires": 86400,
          "record": "myname.yhcna1in4lttygsbd8ufc3kpg89s8mr2f57q5in264q.onetimedns.net",
          "status": "OK",
          "value": "228.89.121.90"
        }

Keep your IP updated using Linux:

        echo '*/5 * * * * nobody curl "https://onetimedns.net/set?name=myname&secret=random_string"' > /etc/cron.d/onetimedns

Or using OpenWRT (you should [enable cron](http://wiki.openwrt.org/doc/howto/notuci.config#etccrontabsroot) first):

        echo '*/5 * * * * wget -s "https://onetimedns.net/set?name=myname&secret=random_string"' >> /etc/crontabs/root
        /etc/init.d/cron restart

FAQ
---
    Q. How long does my name remain mine?
    A. Well, forever, if you keep requesting our API and don't let anybody know your secret.

    Q. What will happen if I stop requesting?
    A. Your name remains resolvable for 24 hours after your last API request.

    Q. And after those 24 hours?
    A. Without updates, your name will expire in 2 months.

    Q. Your long names are so tedious! Do they have to be that way?
    A. Yes, because the longest parts of the names are a SHA224 of your name, your secret and
       our server's secret. By the way, it means that we do not keep your secret at all.

    Q. I forgot my secret, what should I do?
    A. We do not keep your secret in our database (see above). So you either could register
       another name or wait for 2 months.

    Q. My OpenWRT router doesn't support "curl" command, what should I do?
    A. Use "wget -s" instead.

    Q. I'm getting an error "wget: not an http or ftp url: https://onetimedns.net",
       since OpenWRT's wget doesn't support SSL. May I use http:// instead of https?
    A. By all means, just keep in mind that this way your secret will not be secured during the transfer.

Contact
-------
<https://github.com/haron/onetimedns>
