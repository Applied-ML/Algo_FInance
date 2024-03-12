
class Strategies:
    def gamma_based_strategy(df,train_length,y_test,gamma):
        transaction_dict = {}
        total_profit = [0]*len(y_test)
        transaction_number = 0
        for i in range(len(y_test)):
            if i< len(y_test)-gamma:
                if y_test[i] == 1:
                    transaction_number+=1
                    
                    buy_price  = df['Close'].iloc[train_length+i]
                    sell_price = df['Close'].iloc[train_length+i+gamma]
                    current_profit = buy_price - sell_price
                    total_profit[i] = current_profit
                    information = "Transaction number: "+str(transaction_number) +" Buy Date: "+str(df.index[i]) + " Sell Data: "+str(df.index[i+gamma])+" Profit: "+str(current_profit)

                    transaction_dict.update({transaction_number:information})
        result = sum(total_profit) 

        return transaction_dict,result
        

