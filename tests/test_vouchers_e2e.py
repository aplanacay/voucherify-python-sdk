import datetime
from testUtils import getConfiguredClient, getConfig

voucherify = getConfiguredClient()

testVoucher = {
    "code": "PythonVoucherTest",
    "discount": {
        "type": "AMOUNT",
        "amount_off": 12436
    },
    "category": "PythonTestCategory",
    "start_date": "2016-01-01T00:00:00Z",
    "expiration_date": None,
    "redemption": {
        "quantity": None,
        "redeemed_quantity": 0
    },
    "active": True
}


def test_createExistingVoucher(voucherifyInstance=voucherify.vouchers):
    result = voucherifyInstance.create(testVoucher)
    assert result.get('code') == 400
    assert result.get('message') == 'Duplicate resource key'


def test_updateVoucher(voucherifyInstance=voucherify.vouchers):
    uniquePerRun = str(datetime.datetime.utcnow())
    testVoucher['additional_info'] = uniquePerRun
    result = voucherifyInstance.update(testVoucher)
    assert result.get('additional_info') == uniquePerRun


def test_getVoucher(voucherifyInstance=voucherify.vouchers):
    voucher = voucherifyInstance.get(testVoucher.get('code'))
    assert voucher.get('code') == testVoucher.get('code')


def test_listVouchersFromCategory(voucherifyInstance=voucherify.vouchers):
    filter_params = {
        "limit": 1,
        "category": "PythonTestCategory"
    }
    vouchers = voucherifyInstance.list(filter_params).get('vouchers')
    assert len(vouchers) == 1
    voucher = vouchers[0]
    assert voucher.get('code') == testVoucher.get('code')


def test_disableEnableActiveVoucher(voucherifyInstance=voucherify.vouchers):
    voucher = voucherifyInstance.get(testVoucher.get('code'))
    assert voucher.get('active') is True
    disable_result = voucherifyInstance.disable(testVoucher.get('code'))
    assert voucherifyInstance.get(testVoucher.get('code')).get('active') is False
    assert disable_result.get('active') is False

    enable_result = voucherifyInstance.enable(testVoucher.get('code'))
    assert voucherifyInstance.get(testVoucher.get('code')).get('active') is True
    assert enable_result.get('active') is True


def test_disableEnableVoucherThatDoesntExist(voucherifyInstance=voucherify.vouchers):
    randomVoucherCode = 'oaewhiuraowutehaowuet'

    def testEnable():
        result = voucherifyInstance.enable(randomVoucherCode)
        #  assert result is VoucherifyError
        assert result.get('code') == 404

    def testDisable():
        result = voucherifyInstance.enable(randomVoucherCode)
        #  assert result is VoucherifyError
        assert result.get('code') == 404
    testEnable()
    testDisable()


def test_addBalanceToGiftVoucher():
    giftCode = getConfig()['voucherifyTestGiftVoucher']
    giftVoucher = voucherify.vouchers.get(giftCode)
    initialGift = giftVoucher.get('gift')
    assert giftVoucher.get('type') == 'GIFT_VOUCHER'
    additionalAmount = 10
    voucherify.vouchers.balance.create(giftCode, {"amount": additionalAmount})
    rebalancedVoucherGift = voucherify.vouchers.get(giftCode).get('gift')
    assert initialGift.get('amount') + additionalAmount == rebalancedVoucherGift.get('amount')
    assert initialGift.get('balance') + additionalAmount == rebalancedVoucherGift.get('balance')
