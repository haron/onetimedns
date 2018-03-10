#!/usr/bin/env ruby

require 'rubygems'
require 'rubydns'
require "redis"

$R = Resolv::DNS.new
Name = Resolv::DNS::Name
IN = Resolv::DNS::Resource::IN
IP = "YOUR_SERVER_IP_HERE" # change this
TTL = 300
PORT = 5353

redis = Redis.new

# source: https://github.com/socketry/rubydns/blob/master/examples/soa-dns.rb
RubyDNS::run_server(:listen => [[:udp, "0.0.0.0", PORT]]) do
    # change "onetimedns.net" everywhere below to your actual domain name:
	match("onetimedns.net", IN::SOA) do |transaction|
		transaction.respond!(
            # change these two lines too:
			Name.create("ns1.onetimedns.net."),
			Name.create("root.onetimedns.net."),
			File.mtime(__FILE__).to_i,          # Serial Number
			1200,                               # Refresh Time
			900,                                # Retry Time
			3600000,                            # Maximum TTL / Expiry Time
			172800                              # Minimum TTL
		)
		transaction.append_query!(transaction.question, IN::NS, :section => :authority)
	end

	match("onetimedns.net", IN::NS) do |transaction|
		transaction.respond!(Name.create("ns1.onetimedns.net."))
		transaction.respond!(Name.create("ns2.onetimedns.net.")) # fake NS for the registars that require two nameservers
	end

    match(/^(ns\d\.|www\.)?onetimedns\.net$/i, IN::A) do |transaction|
		transaction.respond!(IP, { :ttl => TTL } )
	end

    match(/^([\w\.]+\.\w+\.onetimedns\.net)$/i, IN::A) do |transaction, match_data|
        name = match_data[1]
        ip = redis.get name
        if ip
            transaction.respond!(ip, { :ttl => TTL } )
        else
            transaction.failure!(:NXDomain)
        end
	end

	otherwise do |transaction|
		# Non-Existant Domain
		transaction.failure!(:NXDomain)
	end
end
