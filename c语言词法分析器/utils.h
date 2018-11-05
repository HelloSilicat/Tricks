#define CHARACTER 100
#define STRING 101
#define TOKENS 102
#define ERROR 103
#define Alphabet 104
#define Underline 105
#define Border 106
#define Operator 107
#define ID 108
#define Digit 109
#define String 110
#define Macro 111
#define Others 999
using namespace std;

typedef struct RESULT {
	vector<string> tokens;
	int line;
	int char_num;
	int comment;
}RESULT;

char borders[7] = {'{','}','(',')','[',']',';'};
char operators[20] = {'<','>','&','+','-','*','/','^','!','=','|','%','.','?',':',',','!'};
string keyword[32]={"auto","break","case","char","const",          
                  "continue","default","do","double","else","extern",
                  "enum","float","for","goto","if","int","long","return",
                  "register","static","short","signed","unsigned",
                  "struct","switch","sizeof","typedef","union",
                  "volatile","void","while"};

string id_table[256];
int id_num = 0;

int id_table_insert(string word) {
	for (int i = 0;i < id_num;i++) {
		if (id_table[i].compare(word) == 0) {
			return i+1;
		}
	}
	id_table[id_num++] = word;
	return id_num;
}

int isKey(string word) {
    for(int i = 0; i < 32; i++)
       if (keyword[i].compare(word)==0)
          return 1;
    return 0;
}

int isBorder(char c) {
	for (int i = 0; i < 7; i++) 
		if (c == borders[i])
			return 1;
	return 0;
}

int isOperator(char c) {
	for (int i = 0; i < 17; i++) 
		if (c == operators[i])
			return 1;
	return 0;
} 

int getCharacterType(char c) {
	if (c >= '0' && c <= '9')
		return Digit;
	else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) 
		return Alphabet;
	else if (c == '_')
		return Underline;
	else if (isBorder(c))
		return Border;
	else if (isOperator(c))
		return Operator;
	else 
		return Others; 
}

int nextChar(FILE *fp, int* col) {
	char c = fgetc(fp);
	int i = 0;
	while (c == ' ' || c == '\t') {
		i++;
		col++;
		c = fgetc(fp);
	}
	if (i > 0) {c = ' '; fseek(fp,-1L,1);col--;}
	return c;
}

int addResult(RESULT* output, string token, char cur_c, int output_type, int c_type, int line, int col) {
	char cons[1024]; col--;
	if (output_type == ERROR) {
		if (cur_c == ' ')
			sprintf(cons, "[Error!] Line %d, Col %d, %s\n",line,col,token.c_str());
		else 
			sprintf(cons, "[Error!] Line %d, Col %d, %s,[%c]\n",line,col,token.c_str(),cur_c);
		output->line = line;
		output->char_num += token.size(); 
		printf("%s",cons);
	}
	else {
		if (c_type == Border) {
			sprintf(cons, "Line %d: < 边界符：%c >\n",line,cur_c);
			output->char_num += 1;
		}
		else if (c_type == Operator) {
			if (cur_c == ' ')
				sprintf(cons, "Line %d: < 操作符：%s >\n",line,token.c_str());
			else {
				sprintf(cons, "Line %d: < 操作符：%c >\n",line,cur_c);
				output->char_num += 1;
			}
		}
		else if (c_type == ID) {
			if (!isKey(token)) {
				int id = id_table_insert(token);
				sprintf(cons, "Line %d: < 标识符：%s , %d >\n",line,token.c_str(),id);
			}
			else {
				sprintf(cons, "Line %d: < 保留字：%s >\n",line,token.c_str());
			}
		}
		else if (c_type == Digit) {
			sprintf(cons, "Line %d: < 常数: %s >\n",line,token.c_str());
		}
		else if (c_type == String) {
			sprintf(cons, "Line %d: < 字符串：%s >\n",line,token.c_str());
		}
		else if (c_type == Macro) {				
			sprintf(cons, "Line %d: < 预编译语句：%s >\n",line,token.c_str());
		}
		//printf("%s",cons);
		output->line = line;
		output->char_num += token.size();
		output->tokens.push_back(cons);
	}
	
	return 0;
}

int showTokenInfo(vector<string> tokens, int line, int char_num,int comment) {
	/*
	字符串：0  头文件： 1  操作符： 2
	标识符：3  保留字： 4  常数： 5
	边界符：6  宏定义： 7  
	*/
	int info_num[7] = {0};
	string  info_type[7] = {"字符串","预编译语句","操作符","标识符","保留字","常数","边界符"};
	for (int i = 0;i < tokens.size(); i++) {
		for (int j = 0;j<7;j++) {
			if (tokens[i].find(info_type[j]) != string::npos) {
				info_num[j]++;
				break; 
			}
		}
	}
	printf("\n-----------程序信息统计--------------\n");
	printf("行数：%d，非注释字符总数(不包含空白字符)：%d， 注释字符总数(不包含空包字符)：%d\n各类单词个数如下：\n",line,char_num,comment);
	int j = 0; 
	for (int i = 0; i < 7;i++) {
		if (info_num[i]) {
			j++;
			char temp[1024];
			sprintf(temp, "%s: %d", info_type[i].c_str(),info_num[i]);
			printf("%-20s",temp);
			if (j % 3 == 0) printf("\n");
		}
	}
	printf("\n\n-----------记号表--------------------\n");
	for (int i = 0;i < tokens.size();i++) {
		tokens[i].pop_back();
		printf("%-50s",tokens[i].c_str());
		if ((i+1) % 3 == 0) printf("\n");
	}
}




