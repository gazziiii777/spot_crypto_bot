import bitget.bitget_functions
from databases.db_coin_functions import add_coins_bitget
from bingx.bingx_functions import get_all_coins as bingx_coin
from mexc.mexc_functions import get_all_coins as mexc_coins

bitget.bitget_functions.all_coins()
bitget.bitget_functions.all_coins_correct()
add_coins_bitget()
bingx_coin()
mexc_coins()

