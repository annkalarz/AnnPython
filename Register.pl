#!/usr/bin/perl -wT
use CGI
$q = CGI->new;

#Start html file
print "Content-type: text/html\n\n";

#Get the values of the fields
my $fname = $q->param('firstname');
my $lname = $q->param('lastname');
my $uname = $q->param('username');
my $pass1 = $q->param('password');
my $pass2 = $q->param('confirm_password');

#Read members from database and save it in variable @data
my $file = './Database/Members.csv';
open(MEMBERS,'<',$file);
@data = <MEMBERS>;
close MEMBERS;

#Initialize a found label to 0
$found = 0;

#Error message if the passwords do not match
if( $pass1 ne $pass2 )
{
	open(ERR,'<','./Errors/template.html');
	@content = <ERR>;
	foreach $l (@content)
	{
		print $l;
		if(index($l,"<!--Message-->")!=-1)
		{
			#Add the message to template
			print "<h2>Error:</h2>";
			print "The passwords do not match.\n";					
		}
	}
}
#If the passwords matched
else
{
	#Do through the members data
	foreach $line (@data)
	{
		#Each line has the information of a member
		chomp $line;
		#Save each line of code to array @info
		@info = split(/,/,$line);
		#Error if the username already exists
		if( $info[2] eq $uname )
		{
			open(ERR,'<','./Errors/template.html');
			@content = <ERR>;
			foreach $l (@content)
			{
				#Print the line from template
				print $l;
				if(index($l,"<!--Message-->")!=-1)
				{
					#Add the message to error template
					print "<h2>Error:</h2>";
					print "The username already exists.\n";					
				}
			}
			$found = 1;
			break;
		}
	}
	#In case the username does not exist in members usernames
	if( $found==0 )
	{
		#Add the new line with new users's info to members list file
		open(FILE,'>>','./Database/Members.csv');
		@users = <FILE>;
		print FILE "$fname,$lname,$uname,$pass1\n";
		close FILE;

		#Load the home page after the user has been added
		open(NEXT,'<','index.html');
		@data = <NEXT>;
		print "@data";
		close NEXT;
	}
}