document.addEventListener('DOMContentLoaded', () => {
    
    // 1. قائمة الهواتف المحمولة التفاعلية
    const menuBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');
    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = menuBtn.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-xmark');
        });
    }

    // 2. تأثير التمرير للـ Navbar والظهور التدريجي
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if(navbar) navbar.classList.toggle('nav-scrolled', window.scrollY > 50);
        reveal();
    });

    function reveal() {
        document.querySelectorAll(".reveal").forEach(el => {
            if (el.getBoundingClientRect().top < window.innerHeight - 50) {
                el.classList.add("active");
            }
        });
    }
    reveal();

    // 3. العدادات الرقمية للأرقام الكبيرة
    let hasCounted = false;
    function startCounters() {
        document.querySelectorAll('.counter').forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const updateCounter = () => {
                const c = +counter.innerText;
                const increment = target / 150;
                if (c < target) {
                    counter.innerText = `${Math.ceil(c + increment)}`;
                    setTimeout(updateCounter, 12);
                } else { counter.innerText = target; }
            };
            updateCounter();
        });
    }
    window.addEventListener('scroll', () => {
        const statsSec = document.querySelector('.stats-section');
        if(statsSec && statsSec.getBoundingClientRect().top < window.innerHeight && !hasCounted) {
            startCounters(); hasCounted = true;
        }
    });

    // 4. فلترة معرض الأعمال
    const filterBtns = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const val = btn.getAttribute('data-filter');
            portfolioItems.forEach(item => {
                item.style.transform = 'scale(0.8)'; item.style.opacity = '0';
                setTimeout(() => {
                    if (val === 'all' || val === item.getAttribute('data-category')) {
                        item.classList.remove('hide');
                        setTimeout(() => { item.style.transform = 'scale(1)'; item.style.opacity = '1'; }, 50);
                    } else { item.classList.add('hide'); }
                }, 300);
            });
        });
    });

    // 5. التحكم بتبويبات لوحة التحكم (Dashboard Tabs)
    const sidebarBtns = document.querySelectorAll('.sidebar-btn');
    const dashPanes = document.querySelectorAll('.dash-pane');
    sidebarBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            sidebarBtns.forEach(b => b.classList.remove('active'));
            dashPanes.forEach(p => p.classList.remove('active'));
            
            btn.classList.add('active');
            const targetPane = document.getElementById(btn.getAttribute('data-pane'));
            if(targetPane) {
                targetPane.classList.add('active');
                // تفعيل أنيميشن شريط التقدم عند فتح التبويب الخاص به
                if(btn.getAttribute('data-pane') === 'pane-progress') {
                    animateProgressBars();
                }
            }
        });
    });

    function animateProgressBars() {
        document.querySelectorAll('.progress-bar').forEach(bar => {
            const progress = bar.getAttribute('data-progress');
            bar.style.width = progress + '%';
        });
    }

    // 6. نظام محاكاة تعيين المهام للمدير (Admin Project Assignment)
    const assignBtn = document.getElementById('assign-task-btn');
    if(assignBtn) {
        assignBtn.addEventListener('click', () => {
            const project = document.getElementById('assign-project').value;
            const team = document.getElementById('assign-team').value;
            
            alert(`🚀 تم بنجاح تعيين مشروع [${project}] إلى فريق [${team}] وإرسال إشعار فوري لمساحة عملهم!`);
            
            // إضافة رسالة آلية في نظام الدردشة لتأكيد التعيين
            const chatMessages = document.getElementById('chat-messages');
            if(chatMessages) {
                const msg = document.createElement('div');
                msg.className = 'message system';
                msg.innerText = `⚙️ قام المدير بتعيين مهمة جديدة: ${project} إلى ${team}`;
                chatMessages.appendChild(msg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        });
    }

    // 7. غرف الدردشة التفاعلية الفورية للفريق (Cool Chat Functionality)
    const sendChatBtn = document.getElementById('send-chat-btn');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    if(sendChatBtn && chatInput && chatMessages) {
        const sendMessage = () => {
            const text = chatInput.value.trim();
            if(!text) return;

            // رسالتك أنت (Sent)
            const msg = document.createElement('div');
            msg.className = 'message sent';
            msg.innerHTML = `<span class="sender-name">أنت (المدير)</span>${text}`;
            chatMessages.appendChild(msg);
            chatInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // محاكاة رد تفاعلي من الفريق بعد ثانيتين لتجربة حية ومبهرة!
            setTimeout(() => {
                const reply = document.createElement('div');
                reply.className = 'message received';
                reply.innerHTML = `<span class="sender-name">أحمد (مطور الويب)</span>مفهوم جداً يا فندم! بدأنا الآن بربط واجهات العرض بقاعدة البيانات وسينتهي الـ Sprint قبل الوقت المحدد 💻🔥`;
                chatMessages.appendChild(reply);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1800);
        };

        sendChatBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => { if(e.key === 'Enter') sendMessage(); });
    }

    // 8. معالجة نموذج الاتصال (Contact Form Submission)
    const contactForm = document.getElementById('platform-contact-form');
    if(contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = contactForm.querySelector('input[type="text"]').value;
            alert(`✨ شكراً لتواصلك يا ${name}! تم إرسال رسالتك بنجاح وسنقوم بالرد عليك في أقرب وقت.`);
            contactForm.reset();
        });
    }

    // 9. سنة الفوتر
    if(document.getElementById('year')) document.getElementById('year').innerText = new Date().getFullYear();
});