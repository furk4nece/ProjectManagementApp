Projemizde MySQL ve Python kullanarak bir proje yönetim sistemi oluşturmayı hedefledik.

database.py isimli dosyada MySQL ile oluşturulan veritabanının bağlanılması ve bu veritabanının içine tabloların gerekli niteliklerle oluşturulmas sağlanmıştır.

app.py dosyasının çiçinde 3 ana sekme(Prject, Employee, Tasks) için gerekli fonksiyonlar ve arayüz oluşturma komutları ulunmaktadır.

Her bir sekme için 3 ana komut bulunmaktadır ADD, UPDATE ve DELETE bunların yanı sıra her bir işlem sonrası listelerin güncellenmesi için refresh fonksiyonu bulunmaktadır.

Proje sekmesinden proje ekleyip çıkartabilir eklenen projeleri güncelleyip silebilirsiniz. Sistemde bulunan projelere çift tıklayarak seçili projedeki görevler, görevleri yapan kişileri ve görevlerin tamamlanma durumunu görntüleyebilirsiniz.

Employee sekmesinden sisteme çalışanlar ekleyip çıkartabilir ve bunnları güncelleyebilirsiniz. Sistemde bulunan çalışanlara çift tıklayarak çalıştığı projelere ve görevlerine bakabilirsiniz.

Tasks sekmesinden sistemde var olan projeye görevler ekleyebilir bu görevleri yapacak kişileri atayabilirsiniz.

Uygulamada her bir projenin bitiş tarihi geldiğinde tamamlanmamış görev olup olmadığını kontrol eden ve tamamlanmayan görev varsa projenin bitiş tarihini verilen parametreye göre ileri atayan bir fonksiyon da bulunmaktadır.
