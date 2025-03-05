import argparse
from etherscan import ETHerScanLib


def main(block, method, amount):
    print(f"Parameter block: {block}")
    print(f"Parameter method: {method}")
    print(f"Parameter amount: {amount}")
    # ETHerScanLib().run(url="https://etherscan.io/txs",
    #                     block=block,
    #                     method_filter_strings=method,
    #                     amount_filter_mod=amount)


if __name__ == "__main__":
    # ➢ 指定 block 區間 , 且上限為 100 block (ex. 21442021 - 21442120)
    # 工具需支援指抓取特定 Method and/or Amount (0 或 not 0) 的 filter

    parser = argparse.ArgumentParser(
        description="Script that accept 'block','method',")
    parser.add_argument("--block", type=str, required=True,
                        help="Block_range ,must ")
    parser.add_argument("--method", default="", type=str, help="Method")
    parser.add_argument("--amount", default="", type=str,  help="Amount")

    args = parser.parse_args()

    main(args.block, args.method, args.amount)
