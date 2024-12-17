from coffe import app,db
from coffe.model import Item,User,Image,ItemImage,History
from flask import render_template,redirect,url_for,flash,request
from werkzeug.utils import secure_filename
from coffe.froms import RegisterFrom,LoginForm,PurchaseItem,UploadImageForm,AddItemForm,DepositForm
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/')
def homePage():
    depositForm = DepositForm()
    return render_template("homePage.html",depositForm = depositForm)

@app.route('/shop',methods=['GET','POST'])
@login_required
def shopPage():
    depositForm = DepositForm()
    purchaseItem = PurchaseItem()
    uploadImageForm = UploadImageForm()
    if request.method == "POST": 
        if depositForm.validate_on_submit():
            current_user.budget += depositForm.cash.data
            current_user.history(activity = f"You have Successful deposit",activity_type = 'get',cost = depositForm.cash.data)
            flash("Deposit Successful ",'safe')
            return redirect(url_for('shopPage'))
        if purchaseItem.validate_on_submit():
            selected_item = Item.query.filter_by(id = request.form.get('item')).first()
            if selected_item:                
                selected_item.onSale = 1
                flash(f"You have set {selected_item.name} on Sale!","safe")
                db.session.commit()
                return redirect(url_for('shopPage'))
        else:
            flash(purchaseItem.errors,"danger")
            return redirect(url_for('shopPage'))        
        if uploadImageForm.validate_on_submit():
            pic = request.files['pic']
            if pic:
                filename = secure_filename(pic.filename)
                profileImg = Image.query.filter_by(user_id = current_user.id).first()
                profileImg.set_image(img = pic.read() , mimetype =  pic.mimetype, name = filename)
                flash("Upload success",'safe')
                return redirect(url_for('shopPage'))
            else:
                flash("No Image Found",'danger')
                return redirect(url_for('shopPage'))
        else:
            flash(uploadImageForm.errors,"danger")
            return redirect(url_for('shopPage'))
        
    if request.method ==  'GET':
        products = Item.query.filter((Item.owner == current_user.id) & (Item.onSale == 0))
        countOnSale = Item.query.filter((Item.owner == current_user.id) & (Item.onSale == 1)).count()
        image = Image.query.filter_by(user_id = current_user.id).first()
        return render_template("shop.html",countOnSale = countOnSale ,item_packed = products,purchaseItem = purchaseItem, image = image,uploadImageForm = uploadImageForm,depositForm = depositForm)
@app.route('/shop/onsale',methods=['GET','POST'])
@login_required
def onSalePage():
    depositForm = DepositForm()
    purchaseItem = PurchaseItem()
    uploadImageForm = UploadImageForm()
    if request.method == "POST": 
        if depositForm.validate_on_submit():
            current_user.budget += depositForm.cash.data
            current_user.history(activity = f"You have Successful deposit",activity_type = 'get',cost = depositForm.cash.data)
            flash("Deposit Successful ",'safe')
            return redirect(url_for('onSalePage'))
        if purchaseItem.validate_on_submit():
            selected_item = Item.query.filter_by(id = request.form.get('item')).first()
            if selected_item:                
                selected_item.onSale = 0
                flash(f"You have set {selected_item.name} off Sale!","safe")
                db.session.commit()
                return redirect(url_for('onSalePage'))
        else:
            flash(purchaseItem.errors,"danger")
            return redirect(url_for('onSalePage'))        
        if uploadImageForm.validate_on_submit():
            pic = request.files['pic']
            if pic:
                filename = secure_filename(pic.filename)
                profileImg = Image.query.filter_by(user_id = current_user.id).first()
                profileImg.set_image(img = pic.read() , mimetype =  pic.mimetype, name = filename)
                flash("Upload success",'safe')
                return redirect(url_for('onSalePage'))
            else:
                flash("No Image Found",'danger')
                return redirect(url_for('onSalePage'))
        else:
            flash(uploadImageForm.errors,"danger")
            return redirect(url_for('onSalePage'))
        
    if request.method ==  'GET':
        products = Item.query.filter((Item.owner == current_user.id) & (Item.onSale == 1))
        image = Image.query.filter_by(user_id = current_user.id).first()
        return render_template("onSale.html",item_packed = products,purchaseItem = purchaseItem, image = image,uploadImageForm = uploadImageForm,depositForm = depositForm)

@app.route("/history",methods=['GET','POST'])
@login_required
def historyPage():
    depositForm = DepositForm()
    if request.method == 'POST':
        if depositForm.validate_on_submit():
            current_user.budget += depositForm.cash.data
            current_user.history(activity = f"You have Successful deposit",activity_type = 'get',cost = depositForm.cash.data)
            flash("Deposit Successful ",'safe')
            return redirect(url_for('historyPage'))
    if request.method ==  'GET':
        history = History.query.filter_by(user_id = current_user.id).order_by(History.date.desc()).all()
        return render_template("history.html",historys  = history,depositForm = depositForm)
@app.route("/market",methods=['GET','POST'])
@login_required
def marketPage():
    purchaseItem = PurchaseItem()
    depositForm = DepositForm()
    if request.method == 'POST':
        if depositForm.validate_on_submit():
            current_user.budget += depositForm.cash.data
            current_user.history(activity = f"You have Successful deposit",activity_type = 'get',cost = depositForm.cash.data)
            flash("Deposit Successful ",'safe')
            return redirect(url_for('marketPage'))

        if purchaseItem.validate_on_submit():
            return redirect(url_for('buyItemPage',item_id = request.form.get("item_id")))
        else:
            flash(purchaseItem.errors,'danger')

        return redirect(url_for('marketPage'))
    if request.method ==  'GET':
        items = Item.query.filter((Item.onSale == 1) & (Item.owner != current_user.id)).all()
        return render_template("market.html",items = items, itemImage = ItemImage,purchaseForm = purchaseItem, depositForm = depositForm )
@app.route("/register",methods=['GET','POST'])
def registerPage():
    registerFrom = RegisterFrom()
    if registerFrom.validate_on_submit():
        newUser = User(name = registerFrom.username.data
                       ,set_password = registerFrom.password1.data
                       ,email = registerFrom.email.data)
        db.session.add(newUser)
        db.session.commit()
        profileImage = Image(user_id = newUser.id)
        newUser.history(activity = "Welcome you have crate account", activity_type = "infomation", cost=None)
        db.session.add(profileImage)
        db.session.commit()
        login_user(newUser)
        flash(f"Register Sussecss and login as {newUser.name}", 'safe')
        return redirect(url_for('homePage'))
    else:
        for  key,error in registerFrom.errors.items():
            flash(error[0],'danger')
    return render_template('register.html',form=registerFrom)

@app.route('/login',methods=['GET','POST'])
def loginPage():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        account = User.query.filter_by(name = loginForm.userName.data).first()
        if account and account.password_check(loginForm.password.data):
            login_user(account)
            flash(f'Log In Successfully as: {account.name}','safe')
            return redirect(url_for('homePage'))    
        else:
            print(loginForm.errors)
            flash(f"User name and password don't match",'danger')
    else:
        if loginForm.errors:
            flash(f"User name and password don't match",'danger')
    return render_template("login.html",form=loginForm)
@app.route('/logout')
def logoutPage():
    logout_user()
    flash("You have been logged out !!",'info')
    return redirect(url_for("homePage")) 

@app.route('/addProduct',methods=['GET','POST'])
@login_required
def addProductPage():
    depositForm = DepositForm()
    addProForm = AddItemForm()
    if request.method == 'POST':
        if depositForm.validate_on_submit():
            current_user.budget += depositForm.cash.data
            current_user.history(activity = f"You have Successful deposit",activity_type = 'get',cost = depositForm.cash.data)
            flash("Deposit Successful ",'safe')
            return redirect(url_for('addProductPage'))
        if addProForm.validate_on_submit():
            newItem = Item(name=addProForm.itemName.data,
                           price = addProForm.price.data,
                           description = addProForm.description.data,
                           onSale = True)
            db.session.add(newItem)
            db.session.commit()
            newItem.set_owner(current_user.id)
            pic = request.files["pic"]
            if pic:
                filename = secure_filename(pic.filename)
                itemImg = ItemImage(item_id=newItem.id,img = pic.read() , mimetype =  pic.mimetype, name = filename)
                db.session.add(itemImg)
                db.session.commit()
                flash("You Item  has been added successfully","safe")
                return redirect(url_for('marketPage'))
            else:
                flash("Please select an image for your item ","danger")
        return render_template('addProduct.html',addItemForm = addProForm)


    if request.method == "GET":
        return render_template('addProduct.html',addItemForm = addProForm,depositForm = depositForm)
@app.route('/shop/<item_id>',methods=['GET','POST'])
@login_required
def fixItemPage(item_id):
    depositForm = DepositForm()
    addProForm = AddItemForm()
    item = Item.query.filter_by(id=item_id).first()
    itemImage = ItemImage.query.filter_by(item_id = item.id).first()
    if request.method == 'POST':
        if depositForm.validate_on_submit():
            current_user.budget += depositForm.cash.data
            current_user.history(activity = f"You have Successful deposit",activity_type = 'get',cost = depositForm.cash.data)
            flash("Deposit Successful ",'safe')
            return redirect(url_for('fixItemPage'))
        if addProForm.validate_on_submit():
            item.name = addProForm.itemName.data
            item.price = addProForm.price.data
            item.description = addProForm.description.data
            pic = request.files["pic"]
            if pic:
                itemImage.name = secure_filename(pic.filename)
                itemImage.mimetype = pic.mimetype
                itemImage.img = pic.read()
            flash("You change to your Item  has been added successfully","safe")
            current_user.history(activity=f'The Item with the id {item.id} have been change',activity_type='infomation',cost=None)

            return redirect(url_for('shopPage'))
        else:
            flash(addProForm.errors,'danger')
            return redirect(url_for('fixItemPage',item_id = item_id))

    if request.method == "GET":
        addProForm.description.data = item.description
        return render_template('fixItem.html',itemImage = itemImage,item = item,addItemForm = addProForm,depositForm = depositForm)


@app.route("/market/<item_id>",methods=["POST","GET"])
@login_required
def buyItemPage(item_id):

    depositForm = DepositForm()
    purchaseItem = PurchaseItem()
    item = Item.query.filter_by(id = item_id).first()
    owner = User.query.filter_by(id=item.owner).first()
    if request.method =="POST" :
        if depositForm.validate_on_submit() and request.form:
            current_user.budget += depositForm.cash.data
            current_user.history(activity = f"You have Successful deposit",activity_type = 'get',cost = depositForm.cash.data)
            flash("Deposit Successful ",'safe')
            return redirect(url_for('buyItemPage',item_id = item_id))
        if purchaseItem.validate_on_submit():
            if current_user.affordable(item.price):
                    current_user.budget -= (item.price + item.price*5/100)
                    admin = User.query.filter_by(id = 1).first()
                    if owner:
                        owner.budget += item.price
                        owner.history(activity = f"{current_user.name} brought your {item.name}",activity_type="get",cost = item.price)
                        admin.history(activity = f"{current_user.name} brought {owner.name}'s {item.name} you get 5% form their transaction",activity_type="get",cost = item.price*5/100)
                        current_user.history(activity = f"you brought {owner.name}'s {item.name}",activity_type="lost",cost = (item.price + item.price*5/100))
                    else:
                        admin.budget += item.price
                        admin.history(activity = f"{current_user.name} brought your {item.name}",activity_type="get",cost = (item.price + item.price*5/100))
                        current_user.history(activity = f"you brought {admin.name}'s {item.name}",activity_type="lost",cost = (item.price + item.price*5/100))                    
                    item.onSale = False
                    item.set_owner(current_user.id)
                    flash(f"You have bought {item.name}!","safe")
                    return redirect(url_for('marketPage'))
            else:
                flash("Sorry you can't afford that item at the moment", "danger")
                return redirect(url_for('marketPage'))
                
    if request.method =='GET':        
        if owner:
            userImage = Image.query.filter_by(user_id=owner.id).first()
        else:
            userImage =  None
        itemImage = ItemImage.query.filter_by(item_id=item.id).first()
        return  render_template("buyItem.html",
                                item=item , 
                                purchaseForm = purchaseItem,
                                owner = owner,
                                userImage = userImage,
                                itemImage = itemImage,
                                depositForm = depositForm)
