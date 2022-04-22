    @staticmethod
    def winner_selector(give_away,bet_amount):     
        wheel_map=settings.WHEEL_MAP  #WHEEL_MAP=[20,10,5,0,100,50,20,0,3,2,1,0,500,0,20,10,5,0,200,25,15,0,3,2,1,0,1000,0]
        chosen=[]
        #print(len(wheel_map))
        for n in range(len(wheel_map)):
            val_at_n=wheel_map[n]
            if float(give_away)/float(bet_amount) >=float(val_at_n):
                chosen.append((n,val_at_n))   
                         
        return chosen[randint(0,len(chosen)-1)]
    
