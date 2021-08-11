BEGIN{
	printf("%s\n",t)
	printf("FACTOR\n")
	printf("%E\n",0.000005)
	
}
{
	EE[NR]=$1;
}
END{
	for (fi=0; fi<111; fi++){
		for (di=0; di<360; di++){
			printf("%d\t",EE[fi+di*111]/0.000005)
		}
		printf("\n")
	}
	
}
	
