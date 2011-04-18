$:.unshift File.dirname(__FILE__)

require 'finder'


class FinderController
	class << self

		def init
			@finders = {}
		end

		def search path, text
			finder(path).sorted_matches_for(text).join("\n")
		end


		def flush path
			finder(path).flush
		end


		protected

		def finder path
			@finders[path] ||= CommandT::Finder.new path
		end

	end
end

FinderController.init

while true
	command = gets
	command = command.chomp if command
	
	case command
		when 'exit' then
			break
		when 'search' then
			path = gets.chomp
			text = gets.chomp

			print FinderController.search path, text
			print "\n%%last%%"

		when 'ping' then
			print "ok\n"

		when 'flush' then 
			path = gets.chomp
			FinderController.flush path

	end

	print "\n"
	STDOUT.flush
#	STDOUT.flush
end


