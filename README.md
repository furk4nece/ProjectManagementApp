![ProjectDetails](https://github.com/user-attachments/assets/b03a0dbd-2dd7-442e-9a71-f4ba6f44db7d)Projemizde MySQL ve Python kullanarak bir proje yönetim sistemi oluşturmayı hedefledik.

database.py isimli dosyada MySQL ile oluşturulan veritabanının bağlanılması ve bu veritabanının içine tabloların gerekli niteliklerle oluşturulmas sağlanmıştır.

app.py dosyasının çiçinde 3 ana sekme(Prject, Employee, Tasks) için gerekli fonksiyonlar ve arayüz oluşturma komutları ulunmaktadır.

Her bir sekme için 3 ana komut bulunmaktadır ADD, UPDATE ve DELETE bunların yanı sıra her bir işlem sonrası listelerin güncellenmesi için refresh fonksiyonu bulunmaktadır.

Proje sekmesinden proje ekleyip çıkartabilir eklenen projeleri güncelleyip silebilirsiniz. Sistemde bulunan projelere çift tıklayarak seçili projedeki görevler, görevleri yapan kişileri ve görevlerin tamamlanma durumunu görntüleyebilirsiniz.![Project](https://github.com/user-attachments/assets/8ed4cb2e-0f04-4ae4-8ec6-db395ac37145)
![ProjectDetails](https://github.com/user-attachments/assets/9a8abe2d-c7fc-4960-8ca4-0af4f1b6d3d6)
![ProjectDelay](https://github.com/user-attachments/assets/c00cb767-4f47-45d7-a5b9-6113de34d989)



Employee sekmesinden sisteme çalışanlar ekleyip çıkartabilir ve bunnları güncelleyebilirsiniz. Sistemde bulunan çalışanlara çift tıklayarak çalıştığı projelere ve görevlerine bakabilirsiniz.
![Employee](https://github.com/user-attachments/assets/963df3ab-09e6-48ee-9872-cb016c5a36e8)
![EmployeeDetails](https://github.com/user-attachments/assets/c5a427a7-c323-47dc-9a80-6940f07c2aa8)

Tasks sekmesinden sistemde var olan projeye görevler ekleyebilir bu görevleri yapacak kişileri atayabilirsiniz.
![Task](https://github.com/user-attachments/assets/68fe67bd-44fd-4d70-aa4f-fc1c603b11dc)

Uygulamada her bir projenin bitiş tarihi geldiğinde tamamlanmamış görev olup olmadığını kontrol eden ve tamamlanmayan görev varsa projenin bitiş tarihini verilen parametreye göre ileri atayan bir fonksiyon da bulunmaktadır.
