# 상품 정보를 관리하는 Product 클래스 정의
class Product:

    # 클래스 변수: 상품 객체들이 공유하는 다음 상품 번호
    next_id = 1

    # 생성자: 객체 생성 시 상품 정보를 초기화
    def __init__(self, name, price, stock):

        # 인스턴스 변수: 각 상품 객체의 정보 저장
        self.name = name
        self.price = price
        self.stock = stock

        # 현재 상품에 고유 번호 부여
        self.id = Product.next_id

        # 다음 상품을 위해 번호 1 증가
        Product.next_id += 1


# 상품 재고를 감소시키는 메서드
# self: 현재 상품 객체
# quantity: 구매하려는 수량
    def decrease_stock(self, quantity):
    # 1. 현재 재고보다 구매 수량이 많으면 결제 불가
        if self.stock < quantity:
            print("재고가 부족합니다.")
            return False
    
    # 재고가 충분하면 구매 수량만큼 감소
        self.stock -= quantity
    # 재고 감소에 성공했다는 결과 반환하기
        return True
        

# 객체 생성: Product 클래스를 이용해 실제 상품 만들기
product1 = Product("무선 이어폰", 89000, 3)
product2 = Product("텀블러", 15000, 10)
product3 = Product("보조배터리", 32000, 5)
product4 = Product("마우스패드", 9000, 0)
product5 = Product("USB 허브", 18000, 4)

# 상품 객체들을 하나의 리스트로 관리
products = [product1, product2, product3, product4, product5]


# 장바구니를 관리하는 Cart 클래스
class Cart:
    # 빈 장바구니 만들기
    def __init__(self):
        self.items = {}


    # 장바구니에 상품 추가
    def add(self, product_id, quantity):
        # 이미 장바구니에 담긴 수량 확인
        already = self.items.get(product_id, 0)

        # 기존 수량에 새 수량 더하기
        self.items[product_id] = already + quantity

    # 장바구니에서 상품 삭제
    def remove(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            return True
        return False

    # 장바구니 상품 합계 계산
    def total(self, products):
        total = 0

        for product_id, quantity in self.items.items():
            # products는 Product 객체들의 리스트
            product = products[product_id - 1]
            total += product.price * quantity

        return total

    # 장바구니 전체 비우기
    def clear(self):
        self.items.clear()

# 장바구니 객체 생성
cart = Cart()




# Discount 부모 클래스: discount_amount(상품 합계)의 기본값은 0
class Discount:
    # 할인하지 않는 기본 쿠폰
    def discount_amount(self, total):
        return 0
    

# RateDiscount 자식 클래스: 비율 할인, 최대 5,000원 / 원 미만 버림
class RateDiscount(Discount):
    # 상품 합계의 10% 할인 (최대 5,0000원)
    def discount_amount(self, total):
        return min(int(total * 0.1), 5000)
    

# FixedDiscount 자식 클래스: 조건부 정액 할인
class FixedDiscount(Discount):
    # 상품 합계가 20,000원 이상이면 3000원 할인
    def discount_amount(self, total):
        if total >= 20000:
            return 3000
        return 0


    
# 할인 쿠폰 선택
def select_coupon():
    print("1. 쿠폰 없음")
    print("2. 10% 할인 (최대 5,000원)")
    print("3. 3,000원 할인 (20,000원 이상 구매 시)")

    coupon_number = input("쿠폰 번호:")

    if coupon_number == "1":
        print("적용할 쿠폰이 없습니다.")
        return Discount()

    elif coupon_number == "2":
        print("[10% 할인 (최대 5,000원)] 쿠폰을 적용했습니다.")
        return RateDiscount()

    elif coupon_number == "3":
        print("[3,000원 할인 (20,000원 이상 구매 시)] 쿠폰을 적용했습니다.")
        return FixedDiscount()

    else:
        print("올바른 쿠폰 번호를 입력하세요.")
        return None

selected_coupon = Discount() 





# 1. 상품 목록 출력
def show_products():
    for product in products:
        # 재고가 없을 경우
        if product.stock == 0:
            print(f"{product.id}. {product.name} {product.price:>3}원 (품절)")
        else:
            print(f"{product.id}. {product.name} {product.price:>3}원 (재고 {product.stock}개)")


# 2. 담기 출력
def add_cart():
    # 상품 목록을 보여주면서 상품 번호를 입력하라는 창 생성
    # 1. 상품 목록 보여주기
    show_products()

    # 2. 상품 번호 입력받기
    product_id = input("상품 번호: ").strip()

    # 상품 번호가 존재하는 지 확인
    if product_id in ("1", "2", "3", "4", "5"):
        product_id = int(product_id)
        return

    else:
        print("1부터 5 중에서 입력하세요.")
        return False
    
    # TODO [힌트 2 / 중요]: 번호가 올바르지 않으면 아래 for문으로 내려가지
    # 않도록 처리해야 해. 위 if문과 짝이 되는 분기를 생각해 보기.
    # 안내 메시지를 출력한 뒤 함수를 즉시 끝내려면 이전에 배운 키워드 활용!
    # 예: "abc", "7", "" 입력도 직접 테스트해 보기.


    # 입력한 번호와 일치하는 상품 찾기
    for product in products:
        if product_id == product.id:
            # 재고 확인 0개면 "품절"
            if product.stock == 0:
                print("품절된 상품입니다.")
                return
            
            # 수량 입력 -> 남은 수량 확인
            quantity = input("수량: ").strip()

            # TODO [힌트 2]: 입력한 수량이 양의 정수인지 확인하기
            if not quantity.stock() or int(quantity) <= 0:
                print("올바른 수량을 입력해 주세요.")
                return
            quantity = stock(quantity)

            # 문자, 0, 음수를 입력하면 어떻게 처리할까?
            # 검사를 통과한 뒤 정수로 변환하기

            # TODO [힌트 2]: 장바구니에 이미 담긴 수량 확인하기
            # 처음 담는 상품이라면 기존 수량은 0개
            already = cart.get()

            # TODO [힌트 1]: 추가 가능 수량 계산하기
            # 현재 재고 - 이미 담긴 수량

            # TODO [힌트 1]: 요청 수량이 추가 가능 수량보다 많다면?
            # 재고 부족 메시지 출력 후 함수 종료

            # TODO [힌트 2]: 장바구니에 수량 저장하기
            # 이미 담긴 상품이면 기존 수량에 더하기

            # TODO [힌트 1]: 담기 성공 메시지 출력하기

            return  # 임시 종료, 구현한 뒤 다시 확인하기

        

# 3. 빼기 출력
def remove_cart():
    # TODO [힌트 1]: 장바구니가 비었는지 먼저 확인하기
    # TODO [힌트 1]: 담긴 상품을 보여주고 삭제할 상품 번호 입력받기
    # TODO [힌트 2]: 입력한 상품 번호가 딕셔너리에 있는지 확인하기
    # TODO [힌트 2]: 해당 상품의 기록을 딕셔너리에서 없애기
    # 이 과제에서 '빼기'는 수량 1 감소가 아니라 상품 전체 제거.
    pass




# 4. 장바구니 출력
def shopping_cart():
    # [공통 계산 규칙] 장바구니 출력 및 결제에서 사용
    # ① 상품 합계   = sum(가격 × 수량)
    # ② 할인 금액   = 적용한 쿠폰.discount_amount(상품 합계)
    # ③ 배송비      = (① - ②) 가 30,000원 이상이면 0원, 미만이면 3,000원  (장바구니가 비면 0원)
    # ④ 결제 금액   = ① - ② + ③

    # TODO [힌트 1]: 장바구니가 비었다면 안내하고 종료하기
    # TODO [힌트 2]: 상품 번호와 담긴 수량을 차례로 꺼내 출력하기
    # 상품별 금액 = 상품 가격 × 담긴 수량
    # TODO [힌트 2]: 각 상품 금액을 합산해 '상품 합계' 계산하기
    # TODO [힌트 1]: 선택한 쿠폰의 할인 금액을 빼기
    # TODO [힌트 1]: 할인 후 금액이 30,000원 이상이면 배송비 0원
    # 그보다 작으면 3,000원 (단, 빈 장바구니는 배송비 0원)
    # TODO [힌트 1]: 결제 금액 = 상품 합계 - 할인 + 배송비
    # TODO [힌트 2]: 공통 계산을 나중에 함수/메서드로 분리하면
    # 영수증을 출력하는 payment()에서 같은 계산을 다시 쓸 수 있음.
    # 화면 예시:
    # ----------------------------------------
    # 텀블러      x 9        135,000원
    # ----------------------------------------
    # 상품 합계               135,000원
    # 할인                    -5,000원 [10% 할인 (최대 5,000원)]
    # 배송비                        0원
    # 결제 금액               130,000원
    # ----------------------------------------
    pass



# 5. 쿠폰 출력
def select_coupon():

    # STEP 1. 쿠폰 목록 출력
    # TODO [힌트 1]: print()로 쿠폰 3가지 출력하기
    # 1. 쿠폰 없음
    # 2. 10% 할인 (최대 5,000원)
    # 3. 3,000원 할인 (20,000원 이상 구매 시)

    # STEP 2. 쿠폰 번호 입력
    # TODO [힌트 1]: input()으로 "쿠폰 번호: " 입력받기
    # TODO [힌트 1]: 입력값이 "1", "2", "3" 중 하나인지 확인하기
    # TODO [힌트 1]: 잘못된 입력이면 안내 메시지 출력 후 함수 종료

    # STEP 3. 선택한 쿠폰 저장
    # TODO [힌트 2]: 번호에 맞는 쿠폰 객체를 선택하기
    # 힌트: if / elif / else를 활용할 수 있을까?
    # TODO [힌트 2]: 선택한 쿠폰을 한 번에 하나만 보관하기
    # 힌트: 기존 쿠폰이 있다면 새로운 쿠폰으로 교체하기

    # 할인 규칙
    # Discount: 할인 금액 0원
    # RateDiscount: 합계의 10%, 최대 5,000원 (원 미만 버림)
    # FixedDiscount: 20,000원 이상 구매 시 3,000원 할인

    # STEP 4. 적용 결과 출력
    # TODO [힌트 1]: 선택한 쿠폰 이름을 출력하기
    # 출력 예시: [10% 할인 (최대 5,000원)] 쿠폰을 적용했습니다.

    pass

# 출력 예시
# 1. 쿠폰 없음
# 2. 10% 할인 (최대 5,000원)
# 3. 3,000원 할인 (20,000원 이상 구매 시)
# 쿠폰 번호: 2
# [10% 할인 (최대 5,000원)] 쿠폰을 적용했습니다.



# 6. 결제 출력
def payment():
    # 결제 : 영수증 출력 -> 재고 감소 -> 장바구니 비우기 -> 쿠폰 초기화

    # TODO [힌트 1]: 장바구니가 비었다면 결제할 상품이 없다고 안내
    # TODO [힌트 1]: 장바구니 내용을 영수증처럼 출력하기
    # TODO [힌트 2]: 현재 재고에서 '결제한 수량'만큼 차감하기
    # 실제 재고는 담을 때가 아니라 결제할 때 줄어든다는 점 기억!
    # TODO [힌트 2]: 결제가 끝나면 장바구니를 비우고 쿠폰을 초기화하기
    # TODO [힌트 1]: '결제가 완료되었습니다. 감사합니다!' 출력하기
    # TODO [힌트 1]: 다시 1번 메뉴에서 변경된 재고가 보이는지 테스트
    pass

# 출력 예시
# 선택: 6
# (영수증 출력)
# 결제가 완료되었습니다. 감사합니다!


# 다시 1번을 선택한 경우
# 선택: 1
# ...
# 2. 텀블러        15,000원  (재고 1개)     ← 결제 후 재고 감소가 되어야 함
# ...


# 장바구니 타이틀 출력
def show_title():
    print("-"*56)
    print("1.상품목록 2.담기 3.빼기 4.장바구니 5.쿠폰 6.결제 q.종료")
    print("-"*56)

# 타이틀 입력
def ask_title():
    while True:
        show_title()
        choice = input("선택: ").strip()
        if choice == "q":
            break
        # 1. 상품목록
        elif choice == "1":
            show_products()
        # 2. 담기
        elif choice == "2":
            add_cart()
        # 3. 빼기
        elif choice == "3":
            remove_cart()
        # 4. 장바구니
        elif choice == "4":
            shopping_cart()
        # 5. 쿠폰
        elif choice == "5":
            select_coupon()
        # 6. 결제
        elif choice == "6":
            payment()
        else:
            print("해당되는 번호를 입력하세요.")


# 프로그램 시작 : 메뉴 선택 함수 호출
ask_title()