
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_HTML_LINE_LENGTH 200
#define USERNAME_INDICATOR "<!--username-->"

//Handles the log in updates of database files and catalogue page
void addLoggedIn(char u[])
{
	//Add the user to logged in users
	FILE* loggedIn = fopen("./Database/LoggedIn.csv","a");
	fprintf(loggedIn,"%s,",u);
	fclose(loggedIn);
	
	//Add hidden field to the catalogue page and display it
	FILE* cat = fopen("./catalogue.html","rt");
	int i;
	while(!feof(cat))
	{
		char line[MAX_HTML_LINE_LENGTH];
		fgets(line, MAX_HTML_LINE_LENGTH, cat);
		printf("%s", line);
		if( strstr(line, USERNAME_INDICATOR)!=NULL )
		{
			//Add the hidden field to catalogue page
			printf("<input type=\"hidden\" name=\"username\" value=\"%s\">\n",u);
		}
	}
	fclose(cat);
}

int main()
{
	//Print the 
    printf("%s%c%c\n","Content-Type:text/html;charset=iso-8859-1",13,10);

    //Read the username and password that user entered
	char user[MAX_HTML_LINE_LENGTH], pass[MAX_HTML_LINE_LENGTH];	
	char *data, *first, *second;
	int len = atoi(getenv("CONTENT_LENGTH")) + 1;
	data = (char*)calloc(len,sizeof(char));
	fgets(data,len,stdin);
	if( data!=NULL )
	{
		first = strtok(data,"&");
		second = strtok(NULL,"");
		sscanf(first,"username=%s",user);
		sscanf(second,"password=%s",pass);
	}

	//Open the database members file
	FILE* list = fopen("./Database/Members.csv","rt");
	if( list==NULL )
	{
		return 1;
	}
	char line[MAX_HTML_LINE_LENGTH];
	int found = 0;
	char *f, *l, *u, *p;
	fgets(line,MAX_HTML_LINE_LENGTH,list);
	//Loops through the list of members and check for the username
	while( !found )
	{
		if( feof(list)!=0 )
		{
			break;
		}
		f = strtok(line,",");
		l = strtok(NULL,",");
		u = strtok(NULL,",");
		p = strtok(NULL,"\n");
		if( strcmp(user,u)==0 && strcmp(pass,p)==0 )
		{
			found = 1;
			break;
		}
		fgets(line,MAX_HTML_LINE_LENGTH,list);
	}

	if( found ) //If the username was successfully found
	{
		//Proceed to adding the logged in user
		addLoggedIn(user);		
	}
	else	//In case the username does not exist
	{
		//Print the error webpage using template in the errors folder
		FILE* err = fopen("./Errors/template.html","rt");
		while( !feof(err) )
		{
			char line[MAX_HTML_LINE_LENGTH];
			fscanf(err,"%s",line);
			printf("%s\n",line);
			if( strstr(line,"<!--Message-->") )
			{
				printf("<h2>Error:</h2>");
				printf("<p>The username is not found.</p>");
			}
		}
		fclose(err);
	}
	fclose(list);
	return 0;
}