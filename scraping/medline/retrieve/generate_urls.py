urll = 'http://www.ncbi.nlm.nih.gov/sites/pubmed?EntrezSystem2.PEntrez.DbConnector.Cmd=displaychanged&EntrezSystem2.PEntrez.DbConnector.LastQueryKey=1&EntrezSystem2.PEntrez.DbConnector.Term=english&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Entrez_Pager.CurrPage='
urlr = '&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize=200&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Presentation=medline'

for page in xrange(1, 87074):
    print urll + str(page) + urlr
