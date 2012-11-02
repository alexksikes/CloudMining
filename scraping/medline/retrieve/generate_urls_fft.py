urll = 'http://www.ncbi.nlm.nih.gov/sites/pubmed?EntrezSystem2.PEntrez.DbConnector.Cmd=FilterChanged&EntrezSystem2.PEntrez.DbConnector.LastQueryKey=1&EntrezSystem2.PEntrez.DbConnector.Term=english&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Entrez_Filters.CurrFilter=loattrfree%20full%20text&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Entrez_Pager.CurrPage='
urlr = '&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize=200&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Presentation=abstract'

for page in xrange(1, 14613):
    print urll + str(page) + urlr
