import { Token } from "../Main"
import { useEthers, useTokenBalance } from "@usedapp/core"
import { formatUnits } from "@ethersproject/units"
import { BalanceMsg } from "../../components/BalanceMsg"

export interface WalletBalanceProps {
    token: Token
}


export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(address, account)
    const formattedTokenedBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0
    console.log(account)
    console.log(token)
    console.log(tokenBalance?.toString()) // ? means Convert to string if it's not undefined
    return (
        <BalanceMsg
            label={`Your un-staked ${name} balance`}
            tokenImgSrc={image}
            amount={formattedTokenedBalance} />)
}