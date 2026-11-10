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
    def decrease_stock(self, quantity):
    # 현재 재고보다 구매 수량이 많으면 결제 불가
        if self.stock < quantity:
            print("재고가 부족합니다.")
            return False
    # 재고가 충분하면 구매 수량만큼 감소
        self.stock -= quantity
    # 재고 감소에 성공했다는 결과 반환
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

    
# 쿠폰은 기본적으로 선택하지 않은 상태
cart.selected_coupon = Discount()


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

    else:
        print("1부터 5 중에서 입력하세요.")
        return False
    
    # 올바른 상품 번호라면 정수로 바꾼 뒤 다음 단계 진행
    # 잘못된 상품 번호라면 메시지를 출력하고 함수 종료
    # [확인 필요] 위 정상 입력 분기의 return은 삭제해야 다음 단계로 진행됨


    # 입력한 번호와 일치하는 상품 찾기
    for product in products:
        if product_id == product.id:
            # 재고 확인 0개면 "품절"
            if product.stock == 0:
                print("품절된 상품입니다.")
                return
            
            # 수량 입력 -> 남은 수량 확인
            quantity = input("수량: ").strip()

            # 입력 수량이 숫자인지 검사하고 0보다 큰지 확인
            if not quantity.isdigit() or int(quantity) <= 0:
                print("올바른 수량을 입력해 주세요.")
                return
            quantity = int(quantity)


            # 유효한 수량 문자열을 정수로 변환
            # cart.items에서 현재 상품의 기존 담긴 수량 조회
            #           처음 담는 상품이면 0개
            already = cart.items.get(product_id, 0)

            # 추가 가능 수량 = 실제 재고 - 이미 담긴 수량
            # 요청 수량이 추가 가능 수량보다 많으면 안내 후 종료
            # 재고가 충분하면 cart.add(상품 번호, 수량) 호출
            # 상품명과 추가된 수량을 안내

            return  # 임시 종료, 구현한 뒤 흐름에 맞게 정리하기

        

# 3. 빼기 출력
def remove_cart():
    # cart.items가 비어 있다면 안내 후 종료
    # 현재 장바구니의 상품 번호, 이름, 수량 출력
    # 삭제할 상품 번호 입력받고 정수로 변환 가능한지 검사
    # 입력한 번호가 cart.items에 있는지 확인
    # 있으면 cart.remove(상품 번호) 호출 후 삭제 결과 출력
    # 없으면 장바구니에 없는 상품이라고 안내
    # ※ '빼기'는 수량 1 감소가 아니라 해당 상품 전체 제거
    pass




# 4. 장바구니 출력
def shopping_cart():
    # [공통 계산 규칙] 장바구니 출력 및 결제에서 사용
    # ① 상품 합계   = sum(가격 × 수량)
    # ② 할인 금액   = 적용한 쿠폰.discount_amount(상품 합계)
    # ③ 배송비      = (① - ②) 가 30,000원 이상이면 0원, 미만이면 3,000원  (장바구니가 비면 0원)
    # ④ 결제 금액   = ① - ② + ③

    # 장바구니가 비어 있다면 안내 후 종료
    # cart.items의 상품 번호와 수량을 순서대로 꺼냄
    # 상품별 가격 × 수량을 출력
    # cart.total(products)로 상품 합계 계산
    # selected_coupon.discount_amount(상품 합계)로 할인 계산
    # 할인 후 금액이 30,000원 이상이면 배송비 0원, 아니면 3,000원
    # (장바구니가 비었다면 배송비도 0원)
    # 최종 결제 금액 = 상품 합계 - 할인액 + 배송비
    # 상품 합계, 할인액, 배송비, 결제 금액을 정렬하여 출력
    # 화면 예시:
    # ----------------------------------------      print("-"*50)
    # 텀블러      x 9        135,000원
    # ----------------------------------------      print("-"*50)
    # 상품 합계               135,000원
    # 할인                    -5,000원 [10% 할인 (최대 5,000원)]
    # 배송비                        0원
    # 결제 금액               130,000원
    # ----------------------------------------      print("-"*50)
    pass



# 5. 쿠폰 출력
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




# 6. 결제 출력
def payment():
    # 결제 : 영수증 출력 -> 재고 감소 -> 장바구니 비우기 -> 쿠폰 초기화

    # 장바구니가 비어 있다면 안내 후 종료
    # 장바구니의 모든 상품에 대해 재고가 충분한지 먼저 확인
    # 하나라도 부족하면 결제 전체 중단 (재고 차감하지 않음)
    # 장바구니 상품 합계, 쿠폰 할인액, 배송비, 결제 금액 계산
    # 구매 상품과 계산 금액을 영수증 형식으로 출력
    # 모든 재고 검사가 끝난 뒤 상품별 decrease_stock(수량) 호출
    # cart.clear()로 장바구니 비우기
    # 선택 쿠폰을 Discount()로 초기화
    # '결제가 완료되었습니다. 감사합니다!' 출력
    # 다시 상품 목록을 열어 구매한 만큼 재고가 줄었는지 확인
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
            new_coupon = select_coupon()

            if new_coupon is not None:
                cart.selected_coupon = new_coupon
                
        # 6. 결제
        elif choice == "6":
            payment()
        else:
            print("해당되는 번호를 입력하세요.")


# 프로그램 시작 : 메뉴 선택 함수 호출
ask_title()