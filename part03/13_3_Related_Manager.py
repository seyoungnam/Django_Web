# 관계 매니저

# 13.3.1 관계 매니저 클래스를 사용하는 경우
# User:Album=1:N
user.album_set      # album_set은 관계 매니저 클래스의 객체임
album.owner         # owner는 ForeignKey 타입의 필드명

# Album:Publication=N:N
album1.publication_set  # publication_set은 관계 매니저 클래스의 객체
publication1.albums     # albums는 ManyToMayField 타입의 필드명이면서 관계 매니저 객체

# 13.3.2. 관계 매니저 메소드
# add(*objs, bulk=True)
b = Blog.objects.get(id=1)
e = Entry.objects.get(id=234)
b.entry_set.add(e)      # Entry e 객체를 Blog b 객체에 연결

# create(**kwargs)
b = Blog.objects.get(id=1)
e = b.entry_set.create(
    headline = 'Hello',
    body_text = 'Hi',
    pub_date = datetime.date(2020, 3, 31)
    # Entry e 객체를 생성해서, 이와 Blog b 객체와의 관계를 생성함
)

# 위의 코드는 아래와 같다
b = Blog.objects.get(id=1)
e = Entry(
    blog = b,
    headline = 'Hello',
    body_text = 'Hi',
    pub_date = datetime.date(2020, 3, 31),
)
e.save(force_insert=True)

# remove(*objs, bulk=True)
b = Blog.objects.get(id=1)
e = Entry.objects.get(id=234)
b.entry_set.remove(e)   # Blog b 객체에서 Entry e 객체와의 관계를 끊음(e.blog=None과 같음)

# clear(bulk=True)
b = Blog.objects.get(id=1)
b.entry_set.clear()     # remove, clear 모두 상대 객체와의 관계만 끊는 것, 객체 삭제가 아님

# set(objs, bulk=True, clear=False)
new_list = [obj1, obj2, obj3]
e.related_set.set(new_list)     # 내부적으로 add, remove, clear가 적절히 조합되어 실행

# add(), create(), remove(), clear(), set() 메소드들은 실행 즉시 데이터에 반영됨, 즉 save() 필요없음


